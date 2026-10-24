
from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)

# Configuration
DATA_FILE = "/data/data.json"

# Ensure data file exists with empty list
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump([], file)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kastro EFS StatefulSet Demo</title>
    <style>
        /* Global Styles */
        body {
            margin: 0;
            font-family: "Poppins", sans-serif;
            background: linear-gradient(135deg, #141e30, #243b55);
            color: #f8f9fa;
            line-height: 1.6;
        }

        /* Header Section */
        header {
            background: #0f172a;
            padding: 25px;
            text-align: center;
            color: #00e0ff;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .subtitle {
            font-size: 16px;
            color: #aaa;
            margin-top: 5px;
        }

        /* Main Container */
        .container {
            max-width: 900px;
            margin: 40px auto;
            text-align: center;
            padding: 20px;
        }

        /* Form Styles */
        .data-form {
            background: rgba(255, 255, 255, 0.05);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            margin-bottom: 40px;
            backdrop-filter: blur(6px);
            transition: transform 0.2s ease;
        }

        .data-form:hover {
            transform: scale(1.01);
        }

        .form-label {
            font-weight: bold;
            display: block;
            margin: 15px 0 5px;
            font-size: 15px;
            color: #00e0ff;
        }

        .form-input {
            padding: 12px;
            margin: 5px 0;
            border-radius: 10px;
            border: none;
            width: 80%;
            font-size: 14px;
            box-sizing: border-box;
        }

        .submit-button {
            background: linear-gradient(90deg, #00e0ff, #00ff95);
            color: #000;
            padding: 12px 30px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            margin-top: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .submit-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 15px rgba(0, 224, 255, 0.4);
        }

        /* Data Display Section */
        .section-title {
            color: #00ff95;
            margin-bottom: 15px;
        }

        .data-list {
            list-style-type: none;
            padding: 0;
        }

        .data-item {
            background: #1e293b;
            margin: 10px auto;
            padding: 14px;
            border-radius: 12px;
            width: 65%;
            font-size: 16px;
            text-align: left;
            box-shadow: 0 5px 12px rgba(0, 0, 0, 0.3);
            animation: fadeIn 0.5s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* YouTube Section */
        .youtube-section {
            margin-top: 35px;
        }

        .youtube-link {
            font-size: 16px;
            margin-bottom: 10px;
            display: block;
        }

        .youtube-logo {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .youtube-logo:hover {
            transform: scale(1.2) rotate(8deg);
            box-shadow: 0 8px 18px rgba(255, 0, 0, 0.6);
        }

        /* Footer */
        footer {
            margin-top: 60px;
            padding: 20px;
            background: #0f172a;
            text-align: center;
            font-size: 14px;
            color: #aaa;
            border-top: 1px solid #333;
        }

        .highlight {
            color: #00e0ff;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <header>
        🚀 Kastro EFS StatefulSet Demo
        <div class="subtitle">Persistent, Resilient & Scalable</div>
    </header>

    <div class="container">
        <form method="POST" class="data-form">
            <h2>📝 Enter User Data</h2>
            <label class="form-label">Name:</label>
            <input type="text" name="name" class="form-input" required>
            
            <label class="form-label">Age:</label>
            <input type="number" name="age" class="form-input" required>
            
            <label class="form-label">Gender:</label>
            <input type="text" name="gender" class="form-input" required>
            
            <input type="submit" value="Save Data" class="submit-button">
        </form>

        <h2 class="section-title">📋 Stored Data</h2>
        <ul class="data-list">
        {% for entry in data %}
            <li class="data-item">
                <strong>{{ entry['name'] }}</strong> | Age: {{ entry['age'] }} | Gender: {{ entry['gender'] }}
            </li>
        {% endfor %}
        </ul>

        <div class="youtube-section">
            <span class="youtube-link">👉 Learn more at my channel:</span>
            <a href="https://www.youtube.com/@LearnWithKASTRO" target="_blank" aria-label="Visit Kastro's YouTube channel">
                <img src="https://www.freepnglogos.com/uploads/youtube-logo-hd-8.png" 
                     alt="YouTube Channel" 
                     class="youtube-logo">
            </a>
        </div>
    </div>

    <footer>
        <p>This is a <span class="highlight">Stateful Application</span>, developed and deployed by <span class="highlight">Kastro Kiran V</span>.</p>
        <p>Powered by <span class="highlight">AWS EFS + Kubernetes StatefulSet</span>.</p>
    </footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    """Handle main page requests and form submissions."""
    # Load existing data
    with open(DATA_FILE, "r") as file:
        user_data = json.load(file)

    # Process form submission
    if request.method == "POST":
        new_entry = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "gender": request.form.get("gender")
        }
        
        user_data.append(new_entry)
        
        # Save updated data
        with open(DATA_FILE, "w") as file:
            json.dump(user_data, file, indent=2)

    return render_template_string(HTML_TEMPLATE, data=user_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000
