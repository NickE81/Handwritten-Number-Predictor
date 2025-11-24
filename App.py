from flask  import Flask, request, render_template
from keras.saving import load_model
from keras.utils import load_img
import base64

app = Flask(__name__)

model = load_model("model.keras")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["POST"])
def predict():
    img_file = request.files.get("input-file")
    if img_file is None:
        return render_template("predict.html", img = None)
    img_files_as_bytes = img_file.read()
    img = base64.b64encode(img_files_as_bytes).decode("ascii")
    return render_template("predict.html", img = img)

if __name__ == "__main__":
    app.run(debug = True)


"""
Colour Palette:
Dark Blue: #495867
Medium Blue: #577399
Light Blue: #BDD5EA
Ghost White: #F7F7FF
Coral: #FE5F55
"""