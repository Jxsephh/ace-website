from flask import Flask, redirect, url_for, session, request, jsonify,render_template
from flask_oauthlib.client import OAuth

from flask_app import app
app.debug = True

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


    '''
    *  creator 	*  name 	*  start/end times 	*  point value 	*  category 	*  location 	*  users who signed up (emails) 	*  closed flag
    '''
