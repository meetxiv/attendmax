from flask import Flask, request, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Path to the Excel file (adjust the path as necessary)
EXCEL_FILE_PATH = 'prn_records.xlsx'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get PRN input from the form
        prn = request.form["prn"]
        current_time = datetime.now()

        # Create or load the Excel file
        try:
            # Load the existing Excel file into a DataFrame
            df = pd.read_excel(EXCEL_FILE_PATH)
        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame
            df = pd.DataFrame(columns=["PRN", "Timestamp"])

        # Add the new PRN and the current timestamp to the DataFrame
        new_entry = pd.DataFrame([[prn, current_time]], columns=["PRN", "Timestamp"])
        df = pd.concat([df, new_entry], ignore_index=True)

        # Save the DataFrame to the Excel file
        df.to_excel(EXCEL_FILE_PATH, index=False)

        return "PRN submitted successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
