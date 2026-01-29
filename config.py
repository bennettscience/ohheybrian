import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.abspath(os.path.join(basedir, "..", ".env")))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    CORS_ENDPOINT = os.environ.get("CORS_ENDPOINT")
    COMMENTS_ENDPOINT = os.environ.get("COMMENTS_ENDPOINT")

    # Set the general upload path
    UPLOAD_PATH = os.path.join(basedir, "ohheybrian/static/images")

    # Keep files to 3MB or less
    MAX_CONTENT_LENGTH = 3 * 1000 * 1000

    # Set allowed filetypes
    UPLOAD_EXTENSIONS = [".jpg", ".jpeg", ".png"]
