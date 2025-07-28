import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_meeting_id():
    """Generate a VideoSDK meeting ID using the API"""
    
    auth_token = os.getenv('VIDEOSDK_AUTH_TOKEN')
    if not auth_token:
        print("Error: VIDEOSDK_AUTH_TOKEN not found in .env file")
        return None
    
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            meeting_id = data.get('roomId')
            print(f"✅ Meeting ID generated successfully: {meeting_id}")
            return meeting_id
        else:
            print(f"❌ Error generating meeting ID: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return None

if __name__ == "__main__":
    meeting_id = generate_meeting_id()
    
    if meeting_id:
        # Update the .env file with the generated meeting ID
        with open('.env', 'r') as file:
            content = file.read()
        
        # Replace the empty MEETING_ID line
        updated_content = content.replace('MEETING_ID=', f'MEETING_ID={meeting_id}')
        
        with open('.env', 'w') as file:
            file.write(updated_content)
        
        print(f"✅ .env file updated with meeting ID: {meeting_id}")
    else:
        print("❌ Failed to generate meeting ID")
