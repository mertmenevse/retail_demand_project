from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def list_reports():
    reports_dir = "reports"
    reports = []

    if os.path.exists(reports_dir):
        reports = [f for f in os.listdir(reports_dir) if f.endswith(".pdf")]

    html = """
    <html>
        <head>
            <title>Retail Demand Reports</title>
        </head>
        <body>
            <h1>Reports</h1>
            <ul>
                {% for report in reports %}
                    <li><a href="/reports/{{ report }}" target="_blank">{{ report }}</a></li>
                {% endfor %}
            </ul>
        </body>
    </html>
    """

    return render_template_string(html, reports=reports)

@app.route("/reports/<path:filename>")
def download_report(filename):
    from flask import send_from_directory
    return send_from_directory("reports", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
