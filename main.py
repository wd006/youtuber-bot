import json
import random
import os
import time

# Import modules
import image_generator
import video_creator
import youtube_handler

def load_config():
    """Loads the configuration from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)

def get_random_prompt_from_file():
    """Fetches a random prompt from the prompts.json file."""
    try:
        with open("prompts.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        prompts = data.get("prompts", [])
        if not prompts:
            print("⚠️ WARNING: 'prompts.json' is empty or 'prompts' key not found. Using a default prompt.")
            return "A default prompt: a beautiful landscape"
        return random.choice(prompts)
    except FileNotFoundError:
        print("❌ ERROR: 'prompts.json' not found! Terminating program.")
        exit()
    except json.JSONDecodeError:
        print("❌ ERROR: 'prompts.json' is not a valid JSON file! Terminating program.")
        exit()

def run_upload_cycle(config):
    """Executes one full cycle of generating and uploading a video."""
    print("\n" + "="*50)
    print(f"Starting new cycle at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # 1. Get a random prompt
    prompt = get_random_prompt_from_file()
    print(f"📄 Selected Prompt: '{prompt}'")
    
    # 2. Generate image
    image_bytes = image_generator.create_image_from_prompt(
        prompt,
        config["image_model_api"],
        config["huggingface_api_key"]
    )
    if not image_bytes:
        print("❌ Skipping cycle: Could not generate image.")
        return

    # 3. Create static video from image
    video_file = video_creator.create_static_video(
        image_bytes,
        config["video_settings"]["duration_seconds"],
        config["video_settings"]["fps"]
    )
    if not video_file:
        print("❌ Skipping cycle: Could not create video.")
        return
        
    # 4. Upload to YouTube
    yt_config = config["youtube_settings"]
    youtube_service = youtube_handler.get_youtube_service(
        yt_config["client_secrets_file"],
        yt_config["scopes"]
    )
    
    title = yt_config["title_template"].replace("${prompt}", prompt[:80])
    description = yt_config["description_template"].replace("${prompt}", prompt)
    
    upload_successful = youtube_handler.upload_video(
        youtube_service,
        video_file,
        title,
        description,
        yt_config["tags"],
        yt_config["category_id"],
        yt_config["privacy_status"]
    )
    
    # 5. Delete the temporary video file
    if os.path.exists(video_file):
        os.remove(video_file)
        if upload_successful:
            print(f"🗑️ Temporary video file '{video_file}' deleted.")

def main():
    """Main function: controls the scheduler and the main loop."""
    config = load_config()
    scheduler_cfg = config.get("scheduler_settings", {})
    is_scheduler_enabled = scheduler_cfg.get("enabled", False)

    if not is_scheduler_enabled:
        print("🚀 AI Youtuber Bot starting in Single-Run Mode...")
        run_upload_cycle(config)
        print("\n✅ Single run complete.")
    else:
        print("🚀 AI Youtuber Bot starting in Continuous Mode...")
        min_mins = scheduler_cfg.get("min_minutes", 60)
        max_mins = scheduler_cfg.get("max_minutes", 120)
        
        while True:
            run_upload_cycle(config)
            
            # Calculate a new random wait time for the *next* cycle
            wait_minutes = random.randint(min_mins, max_mins)
            wait_seconds = wait_minutes * 60
            
            # Inform the user
            hours, rem_seconds = divmod(wait_seconds, 3600)
            minutes, _ = divmod(rem_seconds, 60)
            next_run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + wait_seconds))

            print("\n" + "-"*50)
            print(f"✅ Cycle complete. Waiting for the next run...")
            print(f"⏳ Wait Time: {wait_minutes} minutes ({int(hours)}h {int(minutes)}m)")
            print(f"⏰ Next Run Scheduled For: {next_run_time}")
            print("-"*50)

            time.sleep(wait_seconds)

if __name__ == "__main__":
    main()