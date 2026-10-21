"""Entry point:  python run.py"""
from app import create_app
from config.settings import settings

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=True)
