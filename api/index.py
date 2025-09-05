#!/usr/bin/env python3
"""
WISDOM Survey Flask Backend - Lightweight Version for Vercel
Optimized for deployment with minimal dependencies
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import statistics

app = Flask(__name__)
CORS(app)  # Enable CORS for your HTML frontend

# Configuration from environment variables (secure for production)
EMAIL_CONFIG = {
    'smtp_server': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.environ.get('SMTP_PORT', '587')),
    'sender_email': os.environ.get('SENDER_EMAIL', ''),
    'sender_password': os.environ.get('SENDER_PASSWORD', ''),
    'recipient_email': os.environ.get('RECIPIENT_EMAIL', '')
}

# Data storage
CSV_FILE = 'wisdom_survey_responses.csv'
JSON_BACKUP_DIR = 'survey_responses'

def initialize_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        headers = [
            'submission_id', 'participant_id', 'age', 'gender', 'education', 
            'submission_timestamp', 'total_score', 'creativity_score', 
            'curiosity_score', 'judgment_score', 'social_score'
        ]
        
        # Add individual question columns
        for i in range(1, 21):
            headers.extend([f'Q{i}_numeric', f'Q{i}_text', f'Q{i}_question'])
        
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def save_to_csv(data):
    """Save survey response to CSV"""
    row_data = [
        data.get('submission_id'),
        data.get('participant_id'),
        data.get('age'),
        data.get('gender'),
        data.get('education'),
        data.get('submission_timestamp'),
        data.get('total_score'),
        data.get('creativity_score'),
        data.get('curiosity_score'),
        data.get('judgment_score'),
        data.get('social_score')
    ]
    
    # Add individual question responses
    responses = data.get('responses', {})
    for i in range(1, 21):
        q_key = f'Q{i}'
        if q_key in responses:
            row_data.extend([
                responses[q_key].get('value'),
                responses[q_key].get('text'),
                responses[q_key].get('question')
            ])
        else:
            row_data.extend(['', '', ''])
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row_data)

def save_json_backup(data):
    """Save JSON backup of response"""
    if not os.path.exists(JSON_BACKUP_DIR):
        os.makedirs(JSON_BACKUP_DIR)
    
    filename = f"{JSON_BACKUP_DIR}/wisdom_survey_{data['participant_id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_email_notification(data):
    """Send email notification with survey response"""
    if not EMAIL_CONFIG['sender_email'] or not EMAIL_CONFIG['sender_password']:
        print("Email not configured - skipping notification")
        return
        
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        msg['Subject'] = f"New WISDOM Survey Response - {data['participant_id']}"
        
        # Email body
        body = f"""
New WISDOM Survey Response Received!

Participant Details:
- ID: {data['participant_id']}
- Age: {data.get('age', 'Not provided')}
- Gender: {data.get('gender', 'Not provided')}
- Education: {data.get('education', 'Not provided')}
- Submission Time: {data['submission_timestamp']}

WISDOM Scores:
- Total Score: {data['total_score']}/100
- Creativity: {data['creativity_score']}/20
- Curiosity: {data['curiosity_score']}/40
- Judgment: {data['judgment_score']}/20
- Social Wisdom: {data['social_score']}/20

View all responses at: {request.host_url}stats
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['recipient_email'], text)
        server.quit()
        
        print(f"Email notification sent for participant {data['participant_id']}")
        
    except Exception as e:
        print(f"Failed to send email: {e}")

def read_csv_data():
    """Read CSV data and return list of responses"""
    if not os.path.exists(CSV_FILE):
        return []
    
    responses = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('total_score'):  # Skip empty rows
                    responses.append({
                        'participant_id': row.get('participant_id'),
                        'age': row.get('age'),
                        'gender': row.get('gender'),
                        'education': row.get('education'),
                        'submission_timestamp': row.get('submission_timestamp'),
                        'total_score': float(row.get('total_score', 0)),
                        'creativity_score': float(row.get('creativity_score', 0)),
                        'curiosity_score': float(row.get('curiosity_score', 0)),
                        'judgment_score': float(row.get('judgment_score', 0)),
                        'social_score': float(row.get('social_score', 0))
                    })
    except Exception as e:
        print(f"Error reading CSV: {e}")
    
    return responses

@app.route('/')
def home():
    """Simple status page"""
    return jsonify({
        'status': 'WISDOM Survey Backend Running',
        'version': '2.0.0-lightweight',
        'endpoints': {
            'submit': '/submit_survey (POST)',
            'stats': '/stats (GET)',
            'download': '/download_csv (GET)',
            'health': '/health (GET)'
        }
    })

@app.route('/health')
def health_check():
    """Health check for deployment platforms"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    """Handle survey submission"""
    try:
        data = request.json
        
        # Add submission metadata
        data['submission_id'] = f"SUB_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}"
        data['submission_timestamp'] = datetime.now().isoformat()
        
        # Save to CSV and JSON backup
        save_to_csv(data)
        save_json_backup(data)
        
        # Send email notification if configured
        send_email_notification(data)
        
        return jsonify({
            'status': 'success',
            'message': 'Survey response saved successfully',
            'submission_id': data['submission_id']
        }), 200
        
    except Exception as e:
        print(f"Error processing submission: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/stats')
def get_stats():
    """Get basic statistics using lightweight calculations"""
    try:
        responses = read_csv_data()
        
        if not responses:
            return jsonify({'total_responses': 0, 'message': 'No responses yet'})
        
        total_scores = [r['total_score'] for r in responses if r['total_score']]
        
        if total_scores:
            stats = {
                'total_responses': len(responses),
                'latest_submission': max(r['submission_timestamp'] for r in responses),
                'average_total_score': round(statistics.mean(total_scores), 2),
                'score_distribution': {
                    'mean': round(statistics.mean(total_scores), 2),
                    'min': int(min(total_scores)),
                    'max': int(max(total_scores))
                }
            }
            
            # Add standard deviation if more than 1 response
            if len(total_scores) > 1:
                stats['score_distribution']['std'] = round(statistics.stdev(total_scores), 2)
            
            return jsonify(stats)
        else:
            return jsonify({'total_responses': len(responses), 'message': 'No valid scores found'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_csv')
def download_csv():
    """Download CSV file"""
    try:
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                csv_content = f.read()
            
            return csv_content, 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename="wisdom_survey_data_{datetime.now().strftime("%Y%m%d")}.csv"'
            }
        else:
            return jsonify({'error': 'No data file found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize on startup
initialize_csv()

# Export the Flask app for Vercel
def handler(request):
    return app(request.environ, lambda *args: None)

# For Vercel deployment - expose the app
app = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
