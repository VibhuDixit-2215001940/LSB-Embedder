from flask import Flask, request, render_template_string, send_file
from stegano import lsb
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>LSB-Embedder</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 700px; margin: auto; padding: 20px; }
    h2 { margin-top: 40px; }
    form { border: 1px solid #ccc; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    input, textarea { margin-top: 10px; display: block; width: 100%; }
    button { margin-top: 10px; padding: 10px 20px; }
  </style>
</head>
<body>
  <h1>🖼️ LSB-Embedder Web UI</h1>

  <h2>🔒 Embed Secret in Image</h2>
  <form action="/embed" method="post" enctype="multipart/form-data">
    <label>Upload Image:</label>
    <input type="file" name="image" accept="image/*" required>
    <label>Secret Text:</label>
    <textarea name="secret" rows="4" required></textarea>
    <button type="submit">Embed & Download</button>
  </form>

  <h2>🔍 Extract Secret from Image</h2>
  <form action="/extract" method="post" enctype="multipart/form-data">
    <label>Upload Image:</label>
    <input type="file" name="image" accept="image/*" required>
    <button type="submit">Extract Text</button>
  </form>

  {% if extracted %}
    <h3>Extracted Secret:</h3>
    <pre>{{ extracted }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/embed", methods=["POST"])
def embed():
    image = request.files["image"]
    secret = request.form["secret"]

    in_path = os.path.join(UPLOAD_FOLDER, "input.png")
    out_path = os.path.join(UPLOAD_FOLDER, "output.png")

    image.save(in_path)
    lsb.hide(in_path, secret).save(out_path)

    return send_file(out_path, as_attachment=True, download_name="stego.png")

@app.route("/extract", methods=["POST"])
def extract():
    image = request.files["image"]
    in_path = os.path.join(UPLOAD_FOLDER, "to_extract.png")
    image.save(in_path)

    secret = lsb.reveal(in_path)
    return render_template_string(HTML, extracted=secret)

if __name__ == "__main__":
    app.run(debug=True)
