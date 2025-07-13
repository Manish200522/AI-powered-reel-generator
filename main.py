from flask import Flask, render_template, request
import os
import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = str(uuid.uuid1())  # Unique ID for each user session
    if request.method == "POST":
            rec_id = request.form.get("uuid") or myid
            desc = request.form.get("text") or ""
            input_files = []

            # ✅ Create the upload directory BEFORE any file or text is written
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
            os.makedirs(upload_path, exist_ok=True)

            # ✅ Save uploaded files
            for key, file in request.files.items():
                print(key, file)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_path, filename))
                    input_files.append(file.filename)

            # ✅ Write the description AFTER folder is guaranteed to exist
                with open(os.path.join(upload_path, "desc.txt"), "w", encoding="utf-8") as f:
                          f.write(desc)
            for fl in input_files:
                 with open(os.path.join(upload_path, "input.txt"), "a", encoding="utf-8") as f:
                    f.write(f"file '{fl}'\nduration 2\n")

    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    reels=os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html",reels=reels)

if __name__ == "__main__":
    app.run(debug=True)
