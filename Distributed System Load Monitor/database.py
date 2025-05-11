import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('system_monitor.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            cpu_percent REAL NOT NULL,
            memory_percent REAL NOT NULL,
            timestamp DATETIME NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_metrics(device_name, cpu_percent, memory_percent):
    conn = sqlite3.connect('system_monitor.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO system_metrics (device_name, cpu_percent, memory_percent, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (device_name, cpu_percent, memory_percent, datetime.now()))
    conn.commit()
    conn.close()

def get_recent_metrics(device_name=None, limit=100):
    conn = sqlite3.connect('system_monitor.db')
    c = conn.cursor()
    if device_name:
        c.execute('''
            SELECT * FROM system_metrics 
            WHERE device_name = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (device_name, limit))
    else:
        c.execute('''
            SELECT * FROM system_metrics 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
    results = c.fetchall()
    conn.close()
    return results 