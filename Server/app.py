from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from database import db, init_db, Client, Metric, Alert
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize database
with app.app_context():
    init_db()

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    client_id = data.get('client_id')
    cpu_usage = data.get('cpu_usage')
    memory_usage = data.get('memory_usage')
    
    # Register client if not exists
    client = Client.query.get(client_id)
    if not client:
        client = Client(id=client_id, name=f"Client-{client_id}")
        db.session.add(client)
    
    # Store metrics
    metric = Metric(
        client_id=client_id,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage
    )
    db.session.add(metric)
    
    # Check for alerts
    if cpu_usage > app.config['CPU_ALERT_THRESHOLD']:
        alert = Alert(
            client_id=client_id,
            metric_type='cpu',
            value=cpu_usage
        )
        db.session.add(alert)
    
    if memory_usage > app.config['MEMORY_ALERT_THRESHOLD']:
        alert = Alert(
            client_id=client_id,
            metric_type='memory',
            value=memory_usage
        )
        db.session.add(alert)
    
    db.session.commit()
    return jsonify({"status": "success"}), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    client_id = request.args.get('client_id')
    minutes = int(request.args.get('minutes', 5))
    
    # Calculate time threshold
    time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
    
    query = Metric.query.filter(Metric.timestamp >= time_threshold)
    
    if client_id and client_id != 'all':
        query = query.filter_by(client_id=client_id)
    
    metrics = query.order_by(Metric.timestamp.asc()).all()
    
    return jsonify([{
        'timestamp': m.timestamp.isoformat(),
        'client_id': m.client_id,
        'cpu_usage': m.cpu_usage,
        'memory_usage': m.memory_usage
    } for m in metrics])

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    minutes = int(request.args.get('minutes', 30))
    time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
    
    alerts = Alert.query.filter(Alert.timestamp >= time_threshold)\
                      .order_by(Alert.timestamp.desc())\
                      .limit(50).all()
    
    return jsonify([{
        'client_id': a.client_id,
        'metric_type': a.metric_type,
        'value': a.value,
        'timestamp': a.timestamp.isoformat()
    } for a in alerts])

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])