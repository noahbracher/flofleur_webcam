from flask import Flask, redirect, abort
import requests
from datetime import datetime

app = Flask(__name__)

def get_latest_image_url():
    url = "https://www.webcam-4insiders.com/services/slideshow.php"

    today = datetime.now().strftime("%Y%m%d")  # z.B. "20250528"

    payload = {
        "mode": "getPictureList",
        "id": "17210",
        "pictable": "7",
        "displaysec": "false",
        "searchdate": today,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.webcam-4insiders.com/de/Wetter-Köniz-Webcam/17210-Webcam-Köniz-Wetter.php",
        "User-Agent": "Mozilla/5.0",
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            return None
        latest_filename = list(data.values())[-1]
        full_url = f"https://www.webcam-4insiders.com/pictures/original/{latest_filename}"
        return full_url
    except Exception as e:
        print(f"Fehler beim Abrufen des Bildes: {e}")
        return None

@app.route("/")
def redirect_to_latest_image():
    url = get_latest_image_url()
    if not url:
        return abort(404, description="Kein Bild gefunden.")
    return redirect(url)