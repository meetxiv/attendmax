from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, timedelta
import pandas as pd
import os

app = Flask(__name__)

# Path to store the Excel file
EXCEL_FILE = "prn_records.xlsx"
user_last_submission = {}  # Dictionary to track user submissions

# Ensure the Excel file exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["PRN", "Timestamp", "IP Address"])
    df.to_excel(EXCEL_FILE, index=False)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/submit_prn', methods=['POST'])
def submit_prn():
    prn = request.form['prn']
    user_ip = request.remote_addr  # Get user IP address

    # Check if user has submitted within the last 30 minutes
    now = datetime.now()
    if user_ip in user_last_submission:
        last_submission_time = user_last_submission[user_ip]
        if now - last_submission_time < timedelta(minutes=30):
            return (
                f"<h1 style='color:red;'>You can submit only once every 30 minutes.</h1>"
                f"<p>Try again later!</p><a href='/'>Go Back</a>"
            )

    # Update the user's last submission time
    user_last_submission[user_ip] = now

    # Record the PRN and timestamp in the Excel file
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["PRN", "Timestamp", "IP Address"])

    new_record = pd.DataFrame([{
        "PRN": prn,
        "Timestamp": now,
        "IP Address": user_ip
    }])

    # Use pd.concat() to add the new record
    df = pd.concat([df, new_record], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return (
        f"<h1>Thank you!</h1><p>Your PRN ({prn}) has been recorded successfully.</p>"
        f"<a href='/'>Go Back</a>"
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
