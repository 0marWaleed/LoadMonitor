from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import database
import json
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize database
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    data = request.json
    database.save_metrics(
        data['device_name'],
        data['cpu_percent'],
        data['memory_percent']
    )
    # Emit the new metrics to all connected clients
    socketio.emit('new_metrics', data)
    return jsonify({'status': 'success'})

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    device_name = request.args.get('device_name')
    metrics = database.get_recent_metrics(device_name)
    return jsonify([{
        'device_name': m[1],
        'cpu_percent': m[2],
        'memory_percent': m[3],
        'timestamp': m[4]
    } for m in metrics])

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0') 