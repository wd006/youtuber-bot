import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_youtube_service(client_secrets_file, scopes):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            creds = flow.run_console()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

def upload_video(service, video_file, title, description, tags, category_id, privacy_status):
    print("--- STEP 3: Upload to YouTube ---")
    try:
        body = {
            "snippet": {"title": title, "description": description, "tags": tags, "categoryId": category_id},
            "status": {"privacyStatus": privacy_status}
        }
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        request = service.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
        response = request.execute()
        print(f"✅ Video successfully uploaded to YouTube! Video ID: {response['id']}")
        print(f"🔗 URL: https://www.youtube.com/watch?v={response['id']}")
        return True
    except Exception as e:
        print(f"❌ An error occurred while uploading to YouTube: {e}")
        return False