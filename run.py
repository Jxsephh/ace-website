from flask import Flask, redirect, url_for, session, request, jsonify,render_template
from flask_oauthlib.client import OAuth

from flask_app import app
app.debug = True

if __name__ == "__main__":
    app.run(debug=True)