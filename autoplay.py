from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Autoplay Video</title>
  <style>
    body { margin: 0; background: black; }
    iframe { width: 100%; height: 100vh; border: none; }
  </style>
</head>
<body>

<iframe id="player"
  src="https://www.youtube.com/embed/wWytd-YLW_c?autoplay=1&mute=1&loop=1&playlist=wWytd-YLW_c"
  allow="autoplay; fullscreen">
</iframe>

<script>
const correctVideo = "wWytd-YLW_c";

function checkVideo() {
    let iframe = document.getElementById("player");
    let currentSrc = iframe.src;

    if (!currentSrc.includes(correctVideo)) {
        iframe.src = "https://www.youtube.com/embed/" + correctVideo + "?autoplay=1&mute=1&loop=1&playlist=" + correctVideo;
    }
}

// prüft alle 2 Sekunden
setInterval(checkVideo, 2000);
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)