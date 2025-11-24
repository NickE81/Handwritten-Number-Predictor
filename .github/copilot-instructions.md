<!-- .github/copilot-instructions.md - guidance for AI coding agents -->
# Copilot guidance — Handwritten Letter Predictor

This project is a small Flask web app that loads a Keras model (`model.keras`) and exposes a minimal UI for uploading images and showing predictions.

Key files & layout
- `App.py`: Flask entrypoint. Loads the model at import time (`load_model("model.keras")`) and defines two routes: `/` (renders `templates/home.html`) and `/predict` (expects `request.files['input-file']` and renders `templates/predict.html`).
- `model.keras`: the serialized Keras model used for predictions.
- `templates/`: Jinja2 templates (`home.html`, `predict.html`).
- `static/`: CSS under `static/css/style.css`.
- `input images/`: project folder that currently holds example inputs.

Big-picture architecture & data flow (what to know)
- Single-process Flask app: the model is loaded once on startup in `App.py`. Changes to model path or reload behavior should be made here.
- Upload flow: the client sends a file using an `<input name="input-file">`; the server presently gets the raw `FileStorage` object via `request.files['input-file']` and passes it to the template. To make predictions, save or stream that file and run the Keras preprocessing + `model.predict`.

Project-specific patterns and gotchas
- Model is loaded synchronously at import time. For larger models, consider lazy-loading inside the `/predict` handler or using a worker if blocking is a concern.
- `keras.utils.load_img` is imported in `App.py` but not yet used. Typical flow: save the uploaded file to disk or convert in-memory to PIL then call `load_img` / preprocess before `model.predict`.
- Templates expect an `img` variable in `predict.html`; the code currently passes the raw upload object to the template instead of a processed image or prediction result. When updating UI, keep template variable names consistent.

Developer workflows (how to run & debug)
- Create a venv and install dependencies inferred from imports: `flask`, `tensorflow` (or `tensorflow-cpu`) which provides `keras`.
  PowerShell example:
  ```powershell
  py -3 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install --upgrade pip
  pip install flask tensorflow
  ```
- Run locally: `python App.py` (Flask debug is enabled in the file). In PowerShell: `python App.py` or `py -3 App.py`.

Small code examples (how to implement a prediction step)
- In `App.py` replace the current `/predict` handler with this pattern (adapt paths and preprocessing to your model):

```python
# get uploaded file
file = request.files['input-file']
file.save('input images/upload.png')
img = load_img('input images/upload.png', color_mode='grayscale', target_size=(28,28))
# convert to array, scale, and run model.predict
import numpy as np
arr = np.asarray(img) / 255.0
arr = arr.reshape((1, 28, 28, 1))
pred = model.predict(arr)
# pass prediction to template
return render_template('predict.html', prediction=pred.tolist(), img_url='/static/placeholder.png')
```

Integration points & maintenance notes
- When replacing the model file, update the path in `App.py` and restart the Flask process. Tests are not present — add lightweight validation if you change input shapes or preprocessing.
- Static assets are served from `static/` and templates from `templates/`. Keep CSS edits in `static/css/style.css`.

What to prioritize when making changes
- Keep the route names and template variable names stable (`home`, `predict`, template variable `img`/`prediction`) to avoid breaking the minimal UI.
- Avoid loading heavyweight models on every request — prefer startup load or background workers depending on traffic.

If you need more context
- Open `App.py` and the two templates in `templates/` to see how UI and variables are wired.
- The model input shape and preprocessing must match the Keras model saved in `model.keras` — inspect model input layers if unsure.

Questions for the repo owner
- Do you want uploaded images persisted under `input images/` or handled in-memory?  
- Should prediction results be JSON API responses (for programmatic use) or remain server-rendered HTML?

If anything here is unclear or incomplete, tell me which file or behavior you'd like expanded and I'll iterate.
