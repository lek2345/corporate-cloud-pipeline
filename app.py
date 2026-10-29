from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Corporate Cloud Portal</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                text-align: center;
                padding: 80px 20px;
            }
            .card {
                background: white;
                padding: 35px;
                border-radius: 12px;
                max-width: 650px;
                margin: auto;
                box-shadow: 0 4px 15px #0001;
            }
            h1 { color: #17365d; }
            .status { color: #16803c; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Corporate Cloud Portal</h1>
            <p>Welcome to our corporate application.</p>
            <p class="status">Application is running!</p>
            <p>Automated deployment with DevOps and CI/CD.</p>
        </div>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "corporate-cloud-pipeline"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)