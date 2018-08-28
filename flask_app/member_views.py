from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from flask_app import app

# login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# inheiriting from UserMixin provides most default implementations for this class
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return f"id:{self.id} name:{self.name} password:{self.password}"

@app.route('/members')
@login_required
def members():
    return "Members only content here."

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == username + "_secret":
            id = username
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)