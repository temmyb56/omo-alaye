from flask import Flask, request, Response
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

@app.route('/api/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    # Get environment variables
    gmail_user = os.environ.get('GMAIL_USER', 'ajayitemmytope2@gmail.com')
    gmail_password = os.environ.get('GMAIL_PASSWORD', 'dsvuyvjzugbwzhsu')
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = gmail_user
        msg['Subject'] = f"Portfolio Contact: {subject}"
        
        # Email body
        email_body = f"""
New message from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
Reply directly to: {email}
        """
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        # Gmail SMTP settings
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        
        # Return success page
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message Sent - Temitope John</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            max-width: 500px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; margin-bottom: 20px; }}
        p {{ color: #666; margin-bottom: 30px; }}
        .back-btn {{
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 50px;
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ Thank You!</h1>
        <p>Your message has been sent successfully! I'll get back to you at <strong>{email}</strong></p>
        <a href="/" class="back-btn">← Back to Portfolio</a>
    </div>
</body>
</html>
        """
        return Response(html_content, mimetype='text/html')
        
    except Exception as e:
        # Return error page
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Error - Temitope John</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
        .error {{ color: #d32f2f; }}
    </style>
</head>
<body>
    <h1 class="error">Oops! Something went wrong</h1>
    <p>Please try again or contact me directly at ajayitemmytope2@gmail.com</p>
    <a href="/">← Back to Portfolio</a>
</body>
</html>
        """
        return Response(error_html, mimetype='text/html', status=500)