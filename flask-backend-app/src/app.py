from flask import Flask
from routes.api import set_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

set_routes(app)

if __name__ == '__main__':
    app.run(debug=True)