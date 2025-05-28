from flask import Flask, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def latest_image():
    url = "https://www.webcam-4insiders.com/de/Wetter-Köniz-Webcam/17210-Webcam-Köniz-Wetter.php"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    image_tag = soup.select_one("img[src*='/pictures/original/7-17210-']")
    if image_tag:
        print(image_tag)
        return redirect("https://www.webcam-4insiders.com" + image_tag["src"])
    return "No image found", 404