from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
FILENAME = 'tasks.txt'  # same as your console app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            with open(FILENAME, 'a') as file:
                file.write(task + '\n')
        return redirect(url_for('index'))
    else:
        tasks = []
        if os.path.exists(FILENAME):
            with open(FILENAME, 'r') as file:
                tasks = [line.strip() for line in file.readlines()]
        return render_template('index.html', tasks=tasks)

@app.route('/complete', methods=['POST'])
def complete():
    completed = request.form.getlist('done')
    if completed:
        with open(FILENAME, 'r') as file:
            tasks = file.readlines()

        remaining = [task for i, task in enumerate(tasks) if str(i) not in completed]

        with open(FILENAME, 'w') as file:
            for task in remaining:
                file.write(task)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
