from flask import Flask, request, send_from_directory, redirect
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    # Try to send email to your Gmail
    try:
        msg = MIMEMultipart()
        msg['From'] = 'portfolio@temitope.com'
        msg['To'] = 'ajayitemmytope2@gmail.com'
        msg['Subject'] = f"Portfolio Contact: {subject}"
        
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
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        gmail_user = 'ajayitemmytope2@gmail.com'
        gmail_password = 'dsvuyvjzugbwzhsu'
        
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {gmail_user}")
        
    except Exception as email_error:
        print(f"❌ Email sending failed: {email_error}")
    
    # Save to file as backup
    try:
        with open('contact_messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Date: {__import__('datetime').datetime.now()}\n")
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Message: {message}\n")
            f.write(f"{'='*50}\n")
    except:
        pass
    
    print(f"\n=== NEW MESSAGE FROM: {name} ({email}) ===")
    
    # Just redirect back to portfolio - no error messages
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)