from flask import Flask, render_template, jsonify
from twitter_scraper import XScraper
import json
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__, 
           template_folder='templates',  # Explicitly tell Flask where to find templates
           static_folder='static')       # Explicitly tell Flask where to find static files

# Initialize scraper
scraper = XScraper()

@app.route('/')
def index():
    try:
        return render_template('index.html', username=os.getenv('X_USERNAME'))
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/test_login')
def test_login():
    """Test the X login functionality"""
    try:
        result = scraper.test_login()
        return jsonify({
            'success': result,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500

if __name__ == '__main__':
    print(f"""
    Starting X Scraper Application
    ===================================
    Time (UTC): {datetime.now(timezone.utc)}
    Username: {os.getenv('X_USERNAME')}
    """)
    
    port = int(os.getenv('PORT', 5000))
    # Change host to '0.0.0.0' for production deployment
    app.run(debug=False, host='0.0.0.0', port=port)