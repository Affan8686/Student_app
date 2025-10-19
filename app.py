from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# create table if not exists
def init_db():
    
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        course TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
                       (name, email, course))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Static search

# @app.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('q', '')  # get value from search box
#     conn = sqlite3.connect('students.db')
#     cursor = conn.cursor()

#     # search by name, email, or course (case-insensitive)
#     cursor.execute("""
#         SELECT * FROM students
#         WHERE name LIKE ? OR email LIKE ? OR course LIKE ?
#     """, (f'%{query}%', f'%{query}%', f'%{query}%'))

#     students = cursor.fetchall()
#     conn.close()

#     return render_template('index.html', students=students, search_query=query)

# Dynamic Search
@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM students
        WHERE LOWER(name) LIKE ? OR LOWER(email) LIKE ? OR LOWER(course) LIKE ?
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

