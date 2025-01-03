from flask import Flask, render_template, jsonify
from twitter_scraper import XScraper
import json
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Initialize scraper
scraper = XScraper()

@app.route('/')
def index():
    return render_template('index.html', username=os.getenv('X_USERNAME'))

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
    Username: {os.getenv('PORT')}
    """)
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)