from flask import Flask, redirect, abort
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

def get_latest_image_url():
    url = "https://www.webcam-4insiders.com/services/slideshow.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.webcam-4insiders.com/de/Wetter-Köniz-Webcam/17210-Webcam-Köniz-Wetter.php",
        "User-Agent": "Mozilla/5.0",
    }

    for days_back in range(0, 3):  # Heute, gestern, vorgestern
        date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
        payload = {
            "mode": "getPictureList",
            "id": "17210",
            "pictable": "7",
            "displaysec": "false",
            "searchdate": date,
        }

        try:
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and data:
                latest_path = list(data.values())[-1]
                full_url = f"https://www.webcam-4insiders.com/pictures/original/{latest_path}"
                print(f"[{date}] Bild gefunden: {full_url}")
                return full_url
            else:
                print(f"[{date}] Kein Bild gefunden")
        except Exception as e:
            print(f"[{date}] Fehler beim Abrufen: {e}")

    return None

@app.route("/")
def redirect_to_latest_image():
    url = get_latest_image_url()
    if not url:
        return abort(404, description="Kein Bild gefunden.")
    return redirect(url)