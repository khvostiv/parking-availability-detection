from pathlib import Path

from detector import generate_frames
from flask import Flask, Response, render_template

BACKEND_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BACKEND_DIR / "templates"),
    static_folder=str(BACKEND_DIR / "static"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
