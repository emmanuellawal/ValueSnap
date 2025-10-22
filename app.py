from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Store waitlist emails (in production, use a database)
WAITLIST_FILE = 'waitlist.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/waitlist', methods=['POST'])
def join_waitlist():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({'success': False, 'message': 'Invalid email address'}), 400
        
        # Save to file (in production, use a proper database)
        with open(WAITLIST_FILE, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} | {email}\n")
        
        return jsonify({
            'success': True, 
            'message': 'Thanks for joining! We\'ll notify you when ValueSnap launches.'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

if __name__ == '__main__':
    # Create waitlist file if it doesn't exist
    if not os.path.exists(WAITLIST_FILE):
        open(WAITLIST_FILE, 'w').close()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

