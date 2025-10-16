from flask import Blueprint, render_template, url_for, redirect, request
from app.models import Task
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    tasks = Task.query.all() # Pega todas as tarefas do banco
    return render_template('index.html', tasks=tasks)

@main_bp.route('/add', methods=['POST'])
def add_task():
    return redirect(url_for('main.index'))

@main_bp.route('/update/<int:task_id>')
def update_task(task_id):
    task = Task.query.get(task_id) # Busca a tarefa pelo ID
    task.done = not task.done     # Inverte o status
    db.session.commit()           # Salva a alteração
    return redirect(url_for('main.index'))


@main_bp.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id) # Busca a tarefa
    db.session.delete(task)       # Marca para deletar
    db.session.commit()           # Efetiva a deleção
    return redirect(url_for('main.index'))