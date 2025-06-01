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

    for days_ago in range(0, 3):  # Heute bis 2 Tage zurück
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y%m%d")
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

            if isinstance(data, list) and data:
                latest_filename = data[-1]  # neustes Bild
                image_url = f"https://www.webcam-4insiders.com/pictures/original/{latest_filename}"
                return image_url

        except Exception as e:
            print(f"Fehler beim Abrufen für {date}: {e}")

    return None

@app.route('/')
@app.route('/latest')
def redirect_to_latest_image():
    image_url = get_latest_image_url()
    if image_url:
        return redirect(image_url, code=302)
    else:
        abort(404, description="Kein Bild gefunden in den letzten 3 Tagen.")

if __name__ == '__main__':
    app.run(debug=True)