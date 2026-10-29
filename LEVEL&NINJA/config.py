import os
from urllib.parse import quote_plus


class Config:
    """Configurações principais da aplicação."""

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "chave-secreta-level-ninja",
    )

    # Configurações do banco de dados.
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "cecilssz0")
    DB_NAME = os.getenv("DB_NAME", "level")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://"
        f"{DB_USERNAME}:{quote_plus(DB_PASSWORD)}"
        f"@localhost:3306/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload de imagens dos itens (máx. 5 MB).
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "app",
        "static",
        "uploads",
    )
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
