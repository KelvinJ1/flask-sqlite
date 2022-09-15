from multiprocessing import connection
from flask import Flask, request, jsonify
import json
from database import db
import _sqlite3

app= Flask(__name__)

@app.route("/")
def page_not_found():
    return "<h1>MAIN PAGE, JUST EMPTY</h1>"

@app.route("/getbook", methods=["GET", "POST"])
def books():
    connection=db.get_connection()
    cursor=connection.cursor()

    if request.method== "GET":
        cursor=connection.execute("SELECT * FROM books")
        books= [

            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

        if request.method == "POST":
            new_author = request.form["author"]
            new_lang = request.form["language"]
            new_title = request.form["title"]
            preparedStatemen = """INSERT INTO books (author, language, title)
                    VALUES (?, ?, ?)"""
            cursor = cursor.execute(preparedStatemen, (new_author, new_lang, new_title))
            connection.commit()
            return f"Book with the id: 0 created successfully", 201

    

@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    connection = db.get_connection()
    cursor = connection.cursor()
    book = None

    if request.method == "GET":
        cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        preparedStatement = """UPDATE book
                SET title=?,
                    author=?,
                    language=?
                WHERE id=? """

        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]
        updated_book = {
            "id": id,
            "author": author,
            "language": language,
            "title": title,
        }
        connection.execute(preparedStatement, (author, language, title, id))
        connection.commit()
        return jsonify(updated_book)

    if request.method == "DELETE":
        sql = """ DELETE FROM books WHERE id=? """
        connection.execute(sql, (id,))
        connection.commit()
        return "The book with id: {} has been ddeleted.".format(id), 200



if __name__ == '__main__':
    app.run(debug=True, port=5000)