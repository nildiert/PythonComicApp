#!/usr/bin/python3
"""
Flask App that find the latest comics
"""

from flask import Flask

def create_app():
    """
        Method to create the app
    """
    app = Flask(__name__)
    return app