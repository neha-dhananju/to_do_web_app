from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'todo.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS task_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                list_id INTEGER,
                FOREIGN KEY (list_id) REFERENCES task_lists(id)
            )
        ''')

# Homepage – show all task lists
@app.route('/')
def home():
    with sqlite3.connect(DB_NAME) as conn:
        lists = conn.execute('SELECT id, name FROM task_lists').fetchall()
    return render_template('index.html', lists=lists)

# Add new task list
@app.route('/create_list', methods=['POST'])
def create_list():
    title = request.form.get('list_title') or "Untitled List"
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('INSERT INTO task_lists (name) VALUES (?)', (title,))
    return redirect(url_for('home'))


# View a specific task list
@app.route('/list/<int:list_id>', methods=['GET', 'POST'])
def task_list(list_id):
    with sqlite3.connect(DB_NAME) as conn:
        if request.method == 'POST':
            task_content = request.form.get('task')
            if task_content:
                conn.execute('INSERT INTO tasks (content, list_id) VALUES (?, ?)', (task_content, list_id))
            return redirect(url_for('task_list', list_id=list_id))
        
        tasks = conn.execute('SELECT id, content FROM tasks WHERE list_id = ?', (list_id,)).fetchall()
        list_name = conn.execute('SELECT name FROM task_lists WHERE id = ?', (list_id,)).fetchone()[0]
    
    return render_template('task_list.html', tasks=tasks, list_id=list_id, list_name=list_name)

# Delete a task
@app.route('/delete_task/<int:list_id>/<int:task_id>')
def delete_task(list_id, task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('task_list', list_id=list_id))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
