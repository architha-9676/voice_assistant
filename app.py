# ============================================================
#   app.py - Flask Web Interface for Voice Assistant
#   QSkill Internship | Python Development | Slab 2
# ============================================================

from flask import Flask, render_template, request, jsonify
from assistant import process_command, speak, get_weather, get_news, reminders
import datetime
import threading
import pyttsx3

app = Flask(__name__)

# ============================================================
#   ROUTES
# ============================================================

@app.route('/')
def index():
    now = datetime.datetime.now().strftime('%A, %B %d, %Y | %I:%M %p')
    return render_template('index.html', datetime=now)


@app.route('/command', methods=['POST'])
def command():
    """Process text command from web UI."""
    data     = request.get_json()
    query    = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'No command received!'}), 400
    response = process_command(query)
    # Speak in background thread
    t = threading.Thread(target=speak, args=(response,), daemon=True)
    t.start()
    return jsonify({'response': response, 'query': query})


@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()
    city = data.get('city', 'Hyderabad')
    result = get_weather(city)
    return jsonify({'result': result})


@app.route('/news')
def news():
    result = get_news()
    return jsonify({'result': result})


@app.route('/reminders')
def get_reminders():
    return jsonify({'reminders': reminders})


@app.route('/datetime')
def get_datetime():
    now  = datetime.datetime.now()
    return jsonify({
        'time': now.strftime('%I:%M:%S %p'),
        'date': now.strftime('%A, %B %d, %Y')
    })


if __name__ == '__main__':
    print("=" * 55)
    print("  🤖 JARVIS - Voice Assistant Web App")
    print("  QSkill Internship | Python Development")
    print("  ▶ Open: http://127.0.0.1:5000")
    print("=" * 55)
    app.run(debug=True)
