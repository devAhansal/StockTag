﻿from dotenv import load_dotenv
import os

# Charger les variables à partir du fichier .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
