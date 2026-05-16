from flask import Flask, request, send_file, Response
import edge_tts
import asyncio
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Edge TTS API is running!'

@app.route('/tts', methods=['GET'])
def tts():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'ar-EG-ShakirNeural')
    
    if not text:
        return {'error': 'No text provided'}, 400
    
    tmp_path = tempfile.mktemp(suffix='.mp3')
    
    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_path)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate())
    loop.close()
    
    return send_file(tmp_path, mimetype='audio/mpeg', as_attachment=True, download_name='audio.mp3')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
