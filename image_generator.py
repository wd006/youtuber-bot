import requests
import time

def create_image_from_prompt(prompt, api_url, api_key):
    """Creates an image using the given prompt and returns the image data (bytes)."""
    print("--- STEP 1: Text to Image ---")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}
    
    print(f"🖼️ Model: '{api_url}'")
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 503:
        estimated_time = response.json().get("estimated_time", 30)
        print(f"⏳ Loading image model, please wait for {estimated_time:.0f} seconds...")
        time.sleep(estimated_time)
        response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Image created succesfully")
        return response.content
    else:
        print(f"❌ An error occured while image generation. CODE: {response.status_code}, MESSAGE: {response.text}")
        return None