from flask import Flask, request, jsonify, send_file, render_template
import csv
import os
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "temperature_log.csv"

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_temperature():
    data = request.json
    temperature = data.get('temperature')

    if temperature is None:
        return jsonify({"error": "Temperature value is required"}), 400

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Append data to CSV file
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, temperature])

    return jsonify({"message": "Data logged successfully", "timestamp": timestamp, "temperature": temperature})

@app.route('/download', methods=['GET'])
def download_csv():
    return send_file(LOG_FILE, as_attachment=True)

@app.route('/last_entry', methods=['GET'])
def last_entry():
    try:
        with open(LOG_FILE, mode='r') as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                last_row = reader[-1]
                return jsonify({"timestamp": last_row[0], "temperature": last_row[1]})
            else:
                return jsonify({"error": "No data logged yet"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/temperature_data', methods=['GET'])
def temperature_data():
    try:
        with open(LOG_FILE, mode='r') as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                data = [{"timestamp": row[0], "temperature": float(row[1])} for row in reader[1:][-20:]]
                min_temp = min(d["temperature"] for d in data)
                max_temp = max(d["temperature"] for d in data)
                return jsonify({"min_temp": min_temp, "max_temp": max_temp, "data": data})
            else:
                return jsonify({"error": "No data available"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
