from flask import Flask
from routes.api import set_routes

app = Flask(__name__)

set_routes(app)

if __name__ == '__main__':
    app.run(debug=True)