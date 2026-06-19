import psutil
import time


def terminate_process(pid):
    """Terminates a specific process by its Process ID (PID)."""
    try:
        process = psutil.Process(pid)
        process.terminate() # Safely ask it to close
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False
    

def get_network_usage():
    """Fetches bytes sent and received by each running process."""
    processes_data = {}
    
    # Get initial network counters per process (supported on Windows/Linux)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Fetch network I/O counters for the process
            io_counters = proc.io_counters()
            # io_counters contains read/write bytes, which acts as a great proxy
            # For exact network cards, we can map connections:
            connections = proc.connections(kind='inet')
            
            if connections: # If the process has active internet connections
                # Storing process info
                processes_data[proc.info['pid']] = {
                    'name': proc.info['name'],
                    'status': proc.status()
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            continue
            
    return processes_data

# Quick test snippet
if __name__ == "__main__":
    print("Scanning active internet-facing processes...")
    print(get_network_usage())