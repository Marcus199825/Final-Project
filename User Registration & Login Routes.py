from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy database for storing user data
users = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"}
}


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Check if username is already taken
        if username in users:
            return "Username already exists"
        # Add new user to database (hash password for security)
        users[username] = {"username": username, "password": password}
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Check if username and password match
        if username in users and users[username]["password"] == password:
            # Store user's ID in session
            session['username'] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password"
    return render_template("login.html")


@app.route("/logout")
def logout():
    # Clear the session to log out the user
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
