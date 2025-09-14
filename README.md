# AI Youtuber Bot for YouTube

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: MIT](https://img.shields.io/github/license/wd006/youtuber-bot)](https://opensource.org/licenses/MIT)
[![License: MIT](https://img.shields.io/github/languages/top/wd006/youtuber-bot)](https://opensource.org/licenses/MIT)

This bot automatically generates videos with AI and uploads them using the YouTube API.

This project uses the Hugging Face Inference API for image generation and the official YouTube Data API v3 for uploading. It is designed to be modular, configurable, and easy to set up for your own automated content channels.

---
## ✨ Features

*   **Fully Automated Workflow**: From a simple text prompt to a video on YouTube, the entire process is 100% automated.
*   **Centralized Configuration**: No need to edit the source code. All settings, including API keys, model endpoints, and scheduler timing, are managed in a simple `config.json` file.
*   **Intelligent Scheduler**: 
    *   Run the bot in two modes: a **single run** for testing, or **continuous mode** for autonomous, 24/7 operation.
    *   In continuous mode, it uploads videos at **random intervals** between a configurable minimum and maximum time, creating a more natural upload pattern.
    *   Set `min_minutes` and `max_minutes` to the same value for **fixed-interval** scheduling (e.g., exactly every 24 hours).
*   **Externalized Prompts**: Easily manage and expand your list of content ideas by adding them to the `prompts.json` file without ever touching the core logic.
*   **Dynamic Video Details**: Use templates in the configuration file to automatically generate unique YouTube titles and descriptions for each video, incorporating the original prompt with placeholders like `${prompt}`.
*   **Modular and Extensible Codebase**: The project is broken down into logical modules (`image_generator`, `video_creator`, `youtube_handler`), making it easy to understand, maintain, and extend with new features in the future.

---

## How it Works

The workflow is simple and robust:

1.  **Get Prompt**: Selects a random text prompt.
2.  **Generate Image**: Sends the prompt to the Stability AI model via the Hugging Face API to generate an image.
3.  **Create Video**: Converts the generated image into a static MP4 video of a specified duration using MoviePy.
4.  **Upload to YouTube**: Uploads the video to your YouTube channel using the YouTube Data API, with a title and description generated from a template.

---

## 🚀 Setup and Installation

To get this project running on your own machine, follow these steps.

### 1. Prerequisites

*   Python 3.8 or higher
*   A Google Account with a YouTube channel
*   A Hugging Face Account

### 2. Clone the Repository

```bash
git clone https://github.com/wd006/youtuber-bot.git
cd youtuber-bot
```

### 3. Set Up a Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv
```
And activate it
> On Windows:
```bash
.\venv\Scripts\activate
```
> On macOS/Linux:
```
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Obtain API Credentials

This project requires two sets of credentials:

*   **Google API (YouTube):**
    1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    2.  Create a new project.
    3.  Enable the "YouTube Data API v3".
    4.  Create credentials for an "OAuth 2.0 Client ID" with the application type set to "Desktop app".

    5.  Download the JSON file, rename it to `client_secrets.json`, and place it in the project's root directory.

*   **Hugging Face API:**
    1.  Go to your [Hugging Face profile settings](https://huggingface.co/settings/tokens).
    2.  Create a new Access Token with "write" permissions.
    3.  Copy this token.

---

## ⚙️ Configuration (`config.json`)

All of the bot's behavior is controlled from the `config.json` file. This is your main control panel. Below is a detailed breakdown of each setting.

### 🔑 General Settings

| Setting | Description | Usage & Accepted Values |
| :--- | :--- | :--- |
| `huggingface_api_key` | **Required.** Your personal API key for the Hugging Face service. | Replace the placeholder with the Access Token from your Hugging Face profile. |
| `image_model_api` | The API endpoint of the text-to-image model. | It's best to leave the default (`stabilityai/stable-diffusion-xl-base-1.0`) unless you are an advanced user experimenting with other models. |

---

### ⏰ `scheduler_settings`
This section controls the timing and execution mode of the bot.

| Setting | Description | Usage & Accepted Values |
| :--- | :--- | :--- |
| `enabled` | Controls the bot's operating mode. | **`true`**: Continuous Mode. Runs in an endless loop with waits.<br>**`false`**: Single-Run Mode. Runs only once and then stops. |
| `min_minutes` | The minimum time (in minutes) to wait between upload cycles. | An integer. For a **fixed interval**, set this to the same value as `max_minutes`. |
| `max_minutes` | The maximum time (in minutes) to wait between upload cycles. | An integer. Must be greater than or equal to `min_minutes`. |

---

### 🎬 `video_settings`
Controls the properties of the final video file.

| Setting | Description | Usage & Accepted Values |
| :--- | :--- | :--- |
| `duration_seconds`| The total length of the generated static video. | An integer representing seconds (e.g., `10`). |
| `fps` | Frames Per Second for the output video. | `24` is a standard value. No need to change this for a static image video. |

---

### 📺 `youtube_settings`
Controls everything related to the YouTube upload.

| Setting | Description | Usage & Accepted Values |
| :--- | :--- | :--- |
| `client_secrets_file`| The path to your Google API credentials. | Do not change. Should always be `"client_secrets.json"`. |
| `scopes` | Defines the permissions the script requests from Google. | Do not change. |
| `title_template` | A template for the video's title. The `${prompt}` placeholder will be replaced. | Customize the text around the `${prompt}`. Example: `"AI Art Showcase: ${prompt}"` |
| `description_template`| A template for the video's description. Also supports `${prompt}`. | Customize the text to fit your channel's style. You can add links, hashtags, etc. |
| `tags` | A list of tags that will be added to every uploaded video. | Add or remove strings inside the `[ ... ]` list to improve discoverability. |
| `category_id` | A number representing the YouTube video category. | A string containing a number. Common IDs: `"28"` (Science & Tech), `"24"` (Entertainment), `"10"` (Music). Full list [here](https://developers.google.com/youtube/v3/docs/videoCategories/list). |
| `privacy_status` | Sets the visibility of the video upon upload. | Must be one of these three strings: `"public"`, `"private"`, or `"unlisted"`. |

---

## ⚙️ Usage

Once everything is set up, running the script is straightforward.

1.  Make sure your virtual environment is activated.
2.  Run the main script from the terminal:

    ```bash
    python main.py
    ```

On the very first run, you will be prompted to authenticate with Google. A URL will be displayed in the terminal. Copy this URL into your browser, log in with the Google account that owns your YouTube channel, and grant the requested permissions. You will then be given an authorization code to paste back into the terminal.

After the first successful run, a `token.pickle` file will be created, and you won't need to authenticate again.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

<!------->

## 🤝 Contributing

Contributions are welcome!  
Please feel free to fork the repository, make your changes, and submit a pull request.

<!------->

## 📬 Contact

For questions or support:  

<a href="mailto:githubwd@gmail.com" target="_blank"><img src="https://raw.githubusercontent.com/wd006/wd006/main/contact/mail.png" style="width:111" ></a>

or open an issue on GitHub.