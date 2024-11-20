import requests

def job1():
    # Send the message to the n8n webhook
    n8n_url = "https://margusengso.app.n8n.cloud/webhook/703b38d1-2ba1-45ad-86d2-458031dc1e4f"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        requests.post(n8n_url, json={"the_text": ""}, headers=headers, timeout=10)
        print("Job 1 executed")
    except Exception as e:
        print("Job 1 NOT executed: " + str(e))

