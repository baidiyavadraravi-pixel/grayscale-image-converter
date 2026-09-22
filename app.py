from flask import Flask, render_template, request
from PIL import Image
import io
import base64

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    original_image = None
    grayscale_image = None
    error = None

    if request.method == "POST":

        if "file" not in request.files:
            error = "Please select an image."

        else:
            file = request.files["file"]

            if file.filename == "":
                error = "Please select an image."

            else:
                try:
                    image = Image.open(file)

                    image = image.convert("RGB")

                    gray_image = image.convert("L")

                    # Original image
                    original_buffer = io.BytesIO()
                    image.save(original_buffer, format="JPEG")

                    original_image = base64.b64encode(
                        original_buffer.getvalue()
                    ).decode("utf-8")

                    # Grayscale image
                    gray_rgb = gray_image.convert("RGB")

                    gray_buffer = io.BytesIO()
                    gray_rgb.save(gray_buffer, format="JPEG")

                    grayscale_image = base64.b64encode(
                        gray_buffer.getvalue()
                    ).decode("utf-8")

                except Exception as e:
                    error = "Error: " + str(e)

    return render_template(
        "index.html",
        original_image=original_image,
        grayscale_image=grayscale_image,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)