import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE = os.path.join(BASE_DIR, "database", "campusvision.db")
    SECRET_KEY = "campusvision-secret-key"