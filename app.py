import os
from main import model
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("upload_image.html")

# Route to upload image
@app.route('/upload-image', methods=['POST'])
def upload_image():
    cAPTCHA_data = [0]
    image = request.files["cAPTCHA_image"]
    file_path = os.path.join("./samples/", image.filename)

    predictions = model.predict(file_path)
    cAPTCHA = {'file_name': file_path,'captcha_text': predictions}
    cAPTCHA_data[0] = cAPTCHA
    return render_template("upload_image.html", cAPTCHA_data=cAPTCHA_data)


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory("./samples/", filename)

if __name__ == "__main__":
    app.run()