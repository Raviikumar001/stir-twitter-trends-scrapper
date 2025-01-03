from flask import Flask, render_template, jsonify
from twitter_scraper import XScraper
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import traceback 

# Initialize Flask app
app = Flask(__name__)

# Initialize scraper
scraper = XScraper()

@app.route('/')
def index():
    return render_template('index.html', username=os.getenv('X_USERNAME'))

@app.route('/test_login')
def test_login():
    """Test the X login functionality through proxy"""
    try:
        result = scraper.test_login()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'proxy_server': scraper.proxy_server,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500

if __name__ == '__main__':
    print("\nEnvironment variables check:")
    print(f"PROXYMESH_USERNAME exists: {bool(os.getenv('PROXYMESH_USERNAME'))}")
    print(f"PROXYMESH_PASSWORD exists: {bool(os.getenv('PROXYMESH_PASSWORD'))}")
    print(f"X_USERNAME exists: {bool(os.getenv('X_USERNAME'))}")
    print(f"X_PASSWORD exists: {bool(os.getenv('X_PASSWORD'))}")
    
    print(f"""
    Starting X Scraper Application
    ===================================
    Time (UTC): {datetime.now(timezone.utc)}
    Username: {os.getenv('X_USERNAME')}
    Proxy Server: {scraper.proxy_server}
    """)
    
    app.run(debug=True, host='127.0.0.1', port=5000)

# from flask import Flask, render_template, jsonify
# from twitter_scraper import XScraper
# import json
# from datetime import datetime, timezone
# import os
# from dotenv import load_dotenv
# import traceback 

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize scraper
# scraper = XScraper()

# @app.route('/')
# def index():
#     return render_template('index.html', username=os.getenv('X_USERNAME'))

# @app.route('/test_proxy')
# def test_proxy():
#     """Test the ProxyMesh configuration"""
#     try:
#         success = scraper.test_proxy_connection()
        
#         result = {
#             'success': success,
#             'proxy_server': scraper.proxy_server,
#             'timestamp': datetime.now(timezone.utc).isoformat()
#         }
        
#         return jsonify(result)
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e),
#             'timestamp': datetime.now(timezone.utc).isoformat()
#         }), 500
    



# @app.route('/test_login')
# def test_login():
#     """Test the X login functionality"""
#     try:
#         result = scraper.test_login()
#         return jsonify({
#             'success': result,
#             'timestamp': datetime.now(timezone.utc).isoformat()
#         })
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e),
#             'timestamp': datetime.now(timezone.utc).isoformat()
#         }), 500

# if __name__ == '__main__':
#     print("Environment variables check:")
#     print(f"PROXYMESH_USERNAME exists: {bool(os.getenv('PROXYMESH_USERNAME'))}")
#     print(f"PROXYMESH_PASSWORD exists: {bool(os.getenv('PROXYMESH_PASSWORD'))}")
#     print(f"X_USERNAME exists: {bool(os.getenv('X_USERNAME'))}")
#     app.run(debug=True)
#     print(f"""
#     Starting X Scraper Application
#     ===================================
#     Time (UTC): {datetime.now(timezone.utc)}
#     Username: {os.getenv('X_USERNAME')}
#     """)

    
#     app.run(debug=True, host='127.0.0.1', port=5000)