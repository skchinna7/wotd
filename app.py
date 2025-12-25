from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database if not exists
def init_db():
    conn = sqlite3.connect('words.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT UNIQUE,
            word TEXT NOT NULL,
            meaning TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('words.db')
    c = conn.cursor()
    c.execute('SELECT * FROM words ORDER BY day DESC')
    words = c.fetchall()
    conn.close()
    return render_template('index.html', words=words)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('words.db')
    c = conn.cursor()
    if request.method == 'POST':
        action = request.form.get('action')
        day = request.form.get('day')
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        if action == 'add':
            c.execute('INSERT OR IGNORE INTO words (day, word, meaning) VALUES (?, ?, ?)', (day, word, meaning))
        elif action == 'update':
            c.execute('UPDATE words SET word=?, meaning=? WHERE day=?', (word, meaning, day))
        elif action == 'delete':
            c.execute('DELETE FROM words WHERE day=?', (day,))
        conn.commit()
    c.execute('SELECT * FROM words ORDER BY day DESC')
    words = c.fetchall()
    conn.close()
    return render_template('admin.html', words=words)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
