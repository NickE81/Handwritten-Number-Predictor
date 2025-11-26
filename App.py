from flask  import Flask, request, render_template
from keras.saving import load_model
from keras.utils import load_img, img_to_array
import numpy as np
import base64
from io import BytesIO


app = Flask(__name__)

model = load_model("model.keras")

def make_prediction(img_array):
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis = 1)
    return predicted_class[0]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["POST"])
def predict():
    img_file = request.files.get("input-file")
    if img_file is None:
        return render_template("predict.html", img = None)
    img_as_bytes = img_file.read()
    img = load_img(BytesIO(img_as_bytes), target_size = (28, 28), color_mode = "grayscale")
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis = 0)
    img_array = img_array / 255

    predicted_class = make_prediction(img_array)

    img_decoded = base64.b64encode(img_as_bytes).decode("ascii")
    return render_template("predict.html", img = img_decoded, predicted_class = predicted_class)

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