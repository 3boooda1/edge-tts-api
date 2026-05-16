from flask import Flask, request, send_file
import edge_tts
import asyncio
import tempfile
import os

app = Flask(__name__)

@app.route('/tts', methods=['GET'])
def tts():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'ar-EG-ShakirNeural')
    
    if not text:
        return {'error': 'No text provided'}, 400
    
    async def generate():
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tmp_path = f.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_path)
        return tmp_path
    
    tmp_path = asyncio.run(generate())
    return send_file(tmp_path, mimetype='
