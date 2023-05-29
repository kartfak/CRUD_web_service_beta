import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# sozdanie tablici i obnovlenie dannih
connection = sqlite3.connect('database.db')
connection.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)')
connection.execute('INSERT INTO posts (title, content) VALUES ("First post", "Content for the first post")')
connection.execute('INSERT INTO posts (title, content) VALUES ("Second post", "Content for the second post")')
connection.execute('INSERT INTO posts (title, content) VALUES ("Third post", "Content for the third ppost")')
connection.commit()
connection.close()

# marshrut dlya otobrazheniya vseh zapisey
@app.route('/')
def index():
    connection = sqlite3.connect('database.db')
    cursor = connection.execute("SELECT id, title, content FROM posts")
    posts = cursor.fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# marshrut dlya sozdaniya novoy zapisi
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        connection = sqlite3.connect('database.db')
        connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    return render_template('create.html')

# marshrut dlya obnovleniya zapisi
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        connection = sqlite3.connect('database.db')
        connection.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, id))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    connection = sqlite3.connect('database.db')
    cursor = connection.execute("SELECT id, title, content FROM posts WHERE id = ?", (id,))
    post = cursor.fetchone()
    connection.close()

    return render_template('update.html', post=post)

# marshrut dlya udaleniya zapisi
@app.route('/delete/<int:id>')
def delete(id):
    connection = sqlite3.connect('database.db')
    connection.execute("DELETE FROM posts WHERE id = ?", (id,))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)