from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Simple file-based storage
TODOS_FILE = 'todos.json'

# Predefined courses
COURSES = [
    'React',
    'Python',
    'Java',
    'JavaScript',
    'Node.js',
    'Django',
    'Flask',
    'Spring Boot',
    'Angular',
    'Vue.js',
    'TypeScript',
    'MongoDB',
    'PostgreSQL',
    'Docker',
    'Kubernetes'
]

def load_todos():
    """Load todos from JSON file"""
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to JSON file"""
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/')
def index():
    """Main page showing all todos"""
    todos = load_todos()
    return render_template('index.html', todos=todos, courses=COURSES)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo"""
    title = request.form.get('title', '').strip()
    course = request.form.get('course', '').strip()
    
    if title and course:
        todos = load_todos()
        new_todo = {
            'id': len(todos) + 1,
            'title': title,
            'course': course,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        todos.append(new_todo)
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Delete a todo"""
    todos = load_todos()
    todos = [todo for todo in todos if todo['id'] != todo_id]
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/api/todos')
def api_todos():
    """API endpoint to get all todos"""
    return jsonify(load_todos())

if __name__ == '__main__':
    app.run(debug=True)
