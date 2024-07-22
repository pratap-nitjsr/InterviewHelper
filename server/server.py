from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/save_transcript', methods=['POST'])
def save_transcript():
    data = request.json
    print(data)
    transcript = data.get('transcript')
    print("Check1")
    if transcript:
        print(transcript)
        with open('/tmp/transcript.txt', 'w') as file:
            file.write(transcript)
        return jsonify({'status': 'success', 'message': 'Transcript saved successfully.'}), 200
    return jsonify({'status': 'error', 'message': 'No transcript data provided.'}), 400

@app.route('/transcript', methods=['GET'])
def get_transcript():
    try:
        if (os.path.exists('transcript.txt')):
            print("Hello")
        return send_file('/tmp/transcript.txt', as_attachment=True)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
