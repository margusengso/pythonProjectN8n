from flask_socketio import emit
import requests

def init_sockets(socketio_instance):
    @socketio_instance.on('message')
    def handle_message(msg):
        print(f"Message received: {msg}")

        n8n_url = "https://margusengso.app.n8n.cloud/webhook/703b38d1-2ba1-45ad-86d2-458031dc1e4f"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(n8n_url, json={"the_text": msg}, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()

                if isinstance(data, list) and len(data) > 0:
                    file_info = data[0]
                    file_id = file_info.get("id")
                    if file_id:
                        proxy_url = f"https://pythonprojectn8n.onrender.com/proxy-audio?file_id={file_id}"
                        emit('response', {'status': 'success', 'url': proxy_url})
                    else:
                        emit('response', {'status': 'error', 'message': "No file ID found in the response."})
                else:
                    emit('response', {'status': 'error', 'message': "Unexpected response format from n8n."})
            else:
                emit('response', {'status': 'error', 'message': f"Failed to get a response from n8n. Status code: {response.status_code}"})
        except Exception as e:
            emit('response', {'status': 'error', 'message': f"An error occurred: {str(e)}"})