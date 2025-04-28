from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

REPORTS_FOLDER = "reports"

@app.route('/')
def index():
    files = os.listdir(REPORTS_FOLDER)
    files = [f for f in files if f.endswith('.pdf')]
    files.sort(reverse=True)  # En yeni rapor en üstte
    return render_template_string("""
        <h1>Raporlar </h1>
        <ul>
        {% for file in files %}
            <li><a href="/download/{{ file }}">{{ file }}</a></li>
        {% endfor %}
        </ul>
    """, files=files)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(REPORTS_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
