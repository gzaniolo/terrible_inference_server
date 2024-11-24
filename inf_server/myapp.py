from flask import Flask

app = Flask(__name__)

# Routes needs app and jwt. Only import after app creation.
from app import routes

# In case we are not running with gunicorn
if __name__ == '__main__':
    app.run()