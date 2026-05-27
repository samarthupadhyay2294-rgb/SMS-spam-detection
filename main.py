import os
from backend.app import app

if __name__ == '__main__':
    # Determine port and host for local dev execution
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"SpamShield AI running in local development mode.")
    print(f"Server is listening at: http://{host}:{port}")
    
    app.run(host=host, port=port, debug=True)
