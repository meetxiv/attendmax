import os
from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Path to the Excel file (adjust as necessary)
EXCEL_FILE_PATH = os.path.join(os.getcwd(), 'prn_records.xlsx')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prn = request.form["prn"]
        current_time = datetime.now()

        # Try to load the existing Excel file or create a new one if it doesn't exist
        try:
            df = pd.read_excel(EXCEL_FILE_PATH)
        except FileNotFoundError:
            # If file doesn't exist, create a new DataFrame
            df = pd.DataFrame(columns=["PRN", "Timestamp"])

        # Add the new PRN and timestamp to the DataFrame
        new_entry = pd.DataFrame([[prn, current_time]], columns=["PRN", "Timestamp"])
        df = pd.concat([df, new_entry], ignore_index=True)

        # Save the DataFrame back to the Excel file
        try:
            df.to_excel(EXCEL_FILE_PATH, index=False)
        except Exception as e:
            return f"Error saving data: {e}"

        # Log the PRN in the terminal
        print(f"New PRN added: {prn} at {current_time}")

        return "PRN submitted successfully!"

    return render_template("index.html")


# Run the app with dynamic port and host settings for cloud deployment
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
