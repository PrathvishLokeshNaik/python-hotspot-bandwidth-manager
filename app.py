import customtkinter as ctk
import psutil
import time
import threading

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

class DataSaverApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Data Saver Dashboard")
        self.geometry("650x450")

        # Title Label
        self.label = ctk.CTkLabel(self, text="Real-Time Network Monitor", font=("Arial", 20, "bold"))
        self.label.pack(pady=15)

        # Scrollable Frame for Processes
        self.process_frame = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.process_frame.pack(pady=10)

        # Dictionary to keep track of previous process bytes to calculate speed
        self.last_io_counters = {}
        
        # Start a background thread to update network speeds continuously
        self.running = True
        self.monitor_thread = threading.Thread(target=self.realtime_network_loop, daemon=True)
        self.monitor_thread.start()

    def format_speed(self, bytes_per_sec):
        """Converts raw bytes into a human-readable string (KB/s or MB/s)."""
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec} B/s"
        elif bytes_per_sec < 1024 * 1024:
            return f"{bytes_per_sec / 1024:.1f} KB/s"
        else:
            return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"

    def kill_app(self, pid, button):
        try:
            proc = psutil.Process(pid)
            proc.kill()
            button.configure(text="Killed", state="disabled", fg_color="gray")
        except Exception:
            button.configure(text="Failed", fg_color="red")

    def realtime_network_loop(self):
        """Runs in the background every second to calculate speed deltas."""
        while self.running:
            current_network_apps = []

            # 1. Take a snapshot of current process usage
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Filter for apps that have an active internet connection
                    conns = proc.connections(kind='inet')
                    if conns and proc.info['name'] not in ['System', 'svchost.exe']:
                        pid = proc.info['pid']
                        name = proc.info['name']
                        
                        # Get read/write bytes as a proxy for network movement
                        io = proc.io_counters()
                        total_bytes = io.read_bytes + io.write_bytes
                        
                        current_network_apps.append((pid, name, total_bytes))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.Error):
                    continue

            # 2. Wait exactly 1 second to calculate the 'per second' rate
            time.sleep(1)

            # 3. Process the delta speeds
            ui_data = []
            for pid, name, total_bytes in current_network_apps:
                if pid in self.last_io_counters:
                    # Delta = (Bytes Now - Bytes 1 second ago)
                    bytes_diff = total_bytes - self.last_io_counters[pid]
                    if bytes_diff > 0:  # Only care if it's actively moving data
                        speed_str = self.format_speed(bytes_diff)
                        ui_data.append((pid, name, speed_str))
                
                # Update history map
                self.last_io_counters[pid] = total_bytes

            # 4. Schedule the UI update safely on the main thread
            self.after(0, self.update_ui, ui_data)

    def update_ui(self, ui_data):
        """Refreshes the GUI with new data speeds."""
        # Clear old widgets
        for widget in self.process_frame.winfo_children():
            widget.destroy()

        if not ui_data:
            lbl = ctk.CTkLabel(self.process_frame, text="No active data-consuming apps right now.\n(Listening for background activity...)", font=("Arial", 13))
            lbl.pack(pady=40)
            return

        # Render new speeds
        for pid, name, speed_str in ui_data:
            row_frame = ctk.CTkFrame(self.process_frame)
            row_frame.pack(fill="x", pady=5, padx=5)

            # App Name & PID
            lbl_name = ctk.CTkLabel(row_frame, text=f"{name} (PID: {pid})", font=("Arial", 13, "bold"), width=200, anchor="w")
            lbl_name.pack(side="left", padx=10)

            # Live Speed Badge
            lbl_speed = ctk.CTkLabel(row_frame, text=speed_str, font=("Arial", 13), text_color="#3a86ff", width=120, anchor="e")
            lbl_speed.pack(side="left", padx=20)

            # Kill switch
            kill_btn = ctk.CTkButton(row_frame, text="Kill Process", fg_color="#d90429", hover_color="#b3001b", width=100)
            kill_btn.configure(command=lambda p=pid, b=kill_btn: self.kill_app(p, b))
            kill_btn.pack(side="right", padx=10)

    def destroy(self):
        self.running = False # Cleanly stop background thread when window closes
        super().destroy()

if __name__ == "__main__":
    app = DataSaverApp()
    app.mainloop()