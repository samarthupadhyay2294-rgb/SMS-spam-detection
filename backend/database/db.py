import sqlite3
import json
import os

def get_db_connection(db_path):
    """Establishes an active database connection to the SQLite instance."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    """Initializes the database schema if it doesn't already exist."""
    # Ensure parent directory exists if db_path is not in-memory
    if db_path != ':memory:':
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            risk_level TEXT NOT NULL,
            probability REAL NOT NULL,
            keywords TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(db_path, message, prediction, confidence, risk_level, probability, keywords):
    """Persists a prediction record into the SQLite database."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    keywords_str = json.dumps(keywords) if isinstance(keywords, list) else str(keywords)
    cursor.execute('''
        INSERT INTO predictions (message, prediction, confidence, risk_level, probability, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (message, prediction, confidence, risk_level, probability, keywords_str))
    conn.commit()
    conn.close()

def get_history(db_path, limit=10):
    """Retrieves the last N records from the predictions log table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT message, prediction, confidence, risk_level, probability, keywords, created_at
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        try:
            keywords_list = json.loads(row['keywords'])
        except Exception:
            keywords_list = [k.strip() for k in row['keywords'].split(',')] if row['keywords'] else []
            
        history.append({
            'message': row['message'],
            'prediction': row['prediction'],
            'confidence': row['confidence'],
            'risk_level': row['risk_level'],
            'probability': row['probability'],
            'keywords': keywords_list,
            'created_at': row['created_at']
        })
    return history
