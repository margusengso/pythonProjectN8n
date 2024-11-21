import requests
from flask import jsonify, Response, request

def init_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'Hello n8n project'})

    @app.route('/proxy-audio', methods=['GET'])
    def proxy_audio():
        file_id = request.args.get('file_id')
        google_drive_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(google_drive_url, headers=headers, stream=True)
        if response.status_code == 200:
            return Response(
                response.iter_content(chunk_size=1024),
                content_type='audio/mpeg',
                headers={'Content-Disposition': 'inline'}
            )
        else:
            return Response('Unable to fetch the audio file', status=400)