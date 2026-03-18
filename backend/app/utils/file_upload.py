import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from app.utils.errors import ValidationError


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def save_file_local(file):
    """Save uploaded file to local uploads directory. Returns the file path."""
    if not file or file.filename == "":
        raise ValidationError("No file provided")

    if not allowed_file(file.filename):
        raise ValidationError("File type not allowed. Use PNG, JPG, or JPEG.")

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"

    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, unique_name)
    file.save(filepath)

    return f"/uploads/{unique_name}"
