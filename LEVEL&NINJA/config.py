import os
from urllib.parse import quote_plus


class Config:
    """Configurações principais da aplicação."""

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "chave-secreta-level-board",
    )

    # Configurações do banco de dados.
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "labinfo")
    DB_NAME = os.getenv("DB_NAME", "level")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://"
        f"{DB_USERNAME}:{quote_plus(DB_PASSWORD)}"
        f"@localhost:3306/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
