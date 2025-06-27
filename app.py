"""This module starts an app"""

from app.main import create_app

if __name__ == "__main__":
    start_app = create_app()
    start_app.run()
