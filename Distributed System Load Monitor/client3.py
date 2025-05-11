import psutil
import socket
import time
import requests
import json
import socketio

class SystemMonitorClient:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.device_name = 'User-3'
        self.sio = socketio.Client()
        self.setup_socket_events()

    def setup_socket_events(self):
        @self.sio.event
        def connect():
            print(f"Connected to server as {self.device_name}")

    def get_system_metrics(self):
        return {
            'device_name': self.device_name,
            'cpu_percent': psutil.cpu_percent(interval=2),
            'memory_percent': psutil.virtual_memory().percent
        }

    def send_metrics(self):
        try:
            metrics = self.get_system_metrics()
            response = requests.post(
                f"{self.server_url}/api/metrics",
                json=metrics,
                headers={'X-Device-Name': self.device_name}
            )
            if response.status_code == 200:
                print(f"Metrics sent successfully: {metrics}")
            else:
                print(f"Failed to send metrics: {response.status_code}")
        except Exception as e:
            print(f"Error sending metrics: {e}")

    def run(self, interval=5):
        print(f"Starting system monitor client for {self.device_name}")
        try:
            self.sio.connect(self.server_url, auth={'device_name': self.device_name})
            while True:
                self.send_metrics()
                time.sleep(interval)
        except Exception as e:
            print(f"Error in run loop: {e}")
        finally:
            self.sio.disconnect()

if __name__ == "__main__":
    client = SystemMonitorClient()
    client.run() 