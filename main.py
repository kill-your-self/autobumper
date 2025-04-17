
import requests
import time
import schedule

# User Token
TOKEN = "" 

# Channel ID
CHANNEL_ID = "1360732409217290501"

last_message_id = None

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def delete_message(message_id):
    if not message_id:
        return False
    
    api_url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages/{message_id}"
    
    try:
        response = requests.delete(api_url, headers=headers)
        
        if response.status_code == 204: 
            print(f"[{time.strftime('%H:%M:%S')}] Previous message got deleted.")
            return True
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Error. Code: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error: {str(e)}")
        return False

def send_message():
    """Function sending message 'bump' and deleting the previous one."""
    global last_message_id
    
    if last_message_id:
        delete_message(last_message_id)
    
    message_content = "bump message"
    
    payload = {
        "content": message_content
    }
    
    api_url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_json = response.json()
            last_message_id = response_json.get("id")
            print(f"[{time.strftime('%H:%M:%S')}] Message sent again! ID: {last_message_id}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Error. Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Theres exception: {str(e)}")

def main():
    print("Selfbot is running. It will send message 'bump message' every 10 minutes and deleting the previous one bump.")

    # change time  v  here 
    schedule.every(10).minutes.do(send_message)
    
    send_message()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()