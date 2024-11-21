import requests
from flask_socketio import emit
from os import getenv

def message_received(msg):
    if len(msg) < 1:
        emit('response', {'status': 'error', 'message': "empty string received"})
        return


    n8n_url = "https://margusengso.app.n8n.cloud/webhook/" + str(getenv('N8N_HOOK'))
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(n8n_url, json={"the_text": msg}, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()

            # Since the response is a list, access the first element
            if isinstance(data, list) and len(data) > 0:
                file_info = data[0]
                file_id = file_info.get("id")
                if file_id:
                    proxy_url = f"https://pythonprojectn8n.onrender.com/proxy-audio?file_id={file_id}"
                    reply = {'status': 'success', 'url': proxy_url}
                    emit('response', reply)
                else:
                    emit('response', {'status': 'error', 'message': "No file ID found in the response."})
            else:
                emit('response', {'status': 'error', 'message': "Unexpected response format from n8n."})
        else:
            emit('response', {'status': 'error', 'message': f"Failed to get a response from n8n. Status code: {response.status_code}"})
    except Exception as e:
        emit('response', {'status': 'error', 'message': f"An error occurred: {str(e)}"})
