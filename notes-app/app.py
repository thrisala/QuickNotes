from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# ---------------- DB SETUP ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = c.fetchall()
    conn.close()

    return jsonify(notes)


@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.json
    title = data['title']
    content = data['content']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note added successfully"})


@app.route('/delete_note/<int:id>', methods=['DELETE'])
def delete_note(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


if __name__ == '__main__':
    app.run(debug=True)