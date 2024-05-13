from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Dummy database for storing user data
users = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"}
}

# Dummy database for storing user's book data
user_books = {
    "user1": [],
    "user2": []
}

# Google Books API endpoint
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q="


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            # Successful login
            return redirect(url_for("dashboard", username=username))
        else:
            # Invalid credentials
            return "Invalid username or password"
    return render_template("login.html")


@app.route("/dashboard/<username>")
def dashboard(username):
    if username not in users:
        return "User not found"
    user_books_list = user_books.get(username, [])
    return render_template("dashboard.html", username=username, books=user_books_list)


@app.route("/search", methods=["POST"])
def search_books():
    isbn = request.form["isbn"]
    response = requests.get(GOOGLE_BOOKS_API_URL + "isbn:" + isbn)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            title = book_info.get("title", "")
            authors = ", ".join(book_info.get("authors", []))
            page_count = book_info.get("pageCount", "")
            average_rating = book_info.get("averageRating", "")
            thumbnail_url = book_info.get("imageLinks", {}).get("thumbnail", "")
            return render_template("book_details.html", title=title, authors=authors,
                                   page_count=page_count, average_rating=average_rating,
                                   thumbnail_url=thumbnail_url)
        else:
            return "No book found with the given ISBN"
    else:
        return "Error searching for book"


@app.route("/add_book/<username>", methods=["POST"])
def add_book(username):
    # Dummy function to add book to user's list
    title = request.form["title"]
    # Add book to user's list (database)
    user_books[username].append({"title": title})
    return redirect(url_for("dashboard", username=username))


@app.route("/delete_book/<username>/<book_title>", methods=["POST"])
def delete_book(username, book_title):
    # Dummy function to delete book from user's list
    user_books[username] = [book for book in user_books[username] if book["title"] != book_title]
    return redirect(url_for("dashboard", username=username))


if __name__ == "__main__":
    app.run(debug=True)
