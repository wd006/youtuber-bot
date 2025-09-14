from moviepy.editor import ImageClip
import os

def create_static_video(image_bytes, duration, fps):
    """Creates a static MP4 video from an image."""
    print("--- STEP 2: Create a Static Video from Image ---")
    image_filename = "temp_image.jpg"
    video_filename = "generated_video.mp4"
    
    # Write incoming image data to a temporary file
    with open(image_filename, "wb") as f:
        f.write(image_bytes)
    
    try:
        # Create the video with MoviePy
        clip = ImageClip(image_filename).set_duration(duration)
        clip.write_videofile(video_filename, fps=fps, codec="libx264", logger=None)
        print(f"✅ Static video: '{video_filename}' saved.")
        
        # Delete temporary image file
        os.remove(image_filename)
        return video_filename
    except Exception as e:
        print(f"❌ An error occured while creating video: {e}")
        # Delete temporary file in case of error
        if os.path.exists(image_filename):
            os.remove(image_filename)
        return None