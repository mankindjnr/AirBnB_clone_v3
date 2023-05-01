#!/usr/bin/python3
"""
the teardown
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})

app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_404(error):
    """
    json 404 error message
    """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def tear_down(exception=None):
    """
    storage session termination
    """
    storage.close()


if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    app_port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
