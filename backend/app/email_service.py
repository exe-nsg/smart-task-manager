import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_reminder_email(to_email: str, task_title: str, due_time: str):
    try:
        # Create email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"⏰ Reminder: '{task_title}' is due in 15 minutes!"
        msg["From"] = GMAIL_USER
        msg["To"] = to_email

        # Email body
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #f1f5f9; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h1 style="color: #7c3aed; margin-bottom: 8px;">🧠 Smart Task Manager</h1>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 16px 0;">
                <h2 style="color: #0f172a;"> Task Due in 15 Minutes!</h2>
                <div style="background: #faf7ff; border-left: 4px solid #7c3aed; padding: 16px; border-radius: 8px; margin: 16px 0;">
                    <p style="font-size: 1.1rem; font-weight: 600; color: #0f172a; margin: 0;">{task_title}</p>
                    <p style="color: #64748b; margin: 8px 0 0;">Due at: {due_time}</p>
                </div>
                <p style="color: #475569; line-height: 1.6;">
                    You have 15 minutes to complete this task. 
                    Stay focused and give it your best! 
                </p>
                <div style="background: linear-gradient(135deg, #7c3aed, #3b82f6); padding: 16px; border-radius: 8px; margin-top: 16px;">
                    <p style="color: white; margin: 0; font-style: italic; text-align: center;">
                        "Every expert was once a beginner. You got this!"
                    </p>
                </div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 20px; text-align: center;">
                    Sent by Smart Task Manager
                </p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())

        print(f"Reminder email sent to {to_email} for task: {task_title}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
