import psutil
import requests
import time
import socket
from config import SERVER_URL, MONITOR_INTERVAL

def get_system_metrics():
    """Collect actual CPU and memory usage from your PC"""
    # CPU usage (percentage)
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory usage (percentage)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    
    return {
        'client_id': socket.gethostname(),  # Use hostname as client ID
        'cpu_usage': cpu_percent,
        'memory_usage': memory_percent,
        'timestamp': int(time.time())
    }

def send_metrics(server_url, metrics):
    """Send metrics to the monitoring server"""
    try:
        response = requests.post(
            f"{server_url}/api/data",
            json=metrics,
            timeout=5
        )
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Failed to send metrics: {e}")
        return False

def monitor_loop():
    """Continuous monitoring loop"""
    print(f"Starting system monitor. Sending data to {SERVER_URL}")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            # Get actual system metrics
            metrics = get_system_metrics()
            print(f"Collected metrics - CPU: {metrics['cpu_usage']}%, Memory: {metrics['memory_usage']}%")
            
            # Send to server
            if send_metrics(SERVER_URL, metrics):
                print("Successfully sent metrics to server")
            else:
                print("Failed to send metrics to server")
            
            # Wait for next interval
            time.sleep(MONITOR_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == '__main__':
    monitor_loop()