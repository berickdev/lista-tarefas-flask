from flask import Blueprint, jsonify, request
from .models import Task, db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/tarefas', methods=['GET'])
def get_tarefas():
    tarefas = Task.query.all()
    tarefas_list = [
        {'id':task.id, 'titulo':task.title, 'descricao':task.description, 'concluido':task.done}
        for task in tarefas
    ]

    return jsonify(tarefas_list)

@api_bp.route('/tarefas', methods=['POST'])
def create_tarefa():
    dados = request.get_json()
    if not dados or not 'titulo' in dados:
        return jsonify({'erro': 'O campo título é obrigatório'}), 400

    nova_tarefa = Task(
        title=dados['titulo'],
        description=dados.get('descricao', ''),
        done=dados.get('concluida', False)
    )
    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify({'id': nova_tarefa.id, 'titulo': nova_tarefa.title}), 201

@api_bp.route('/tarefas/<int:id>', methods=['PUT'])
def update_tarefa(id):
    tarefa = Task.query.get_or_404(id)
    dados = request.get_json()

    tarefa.title = dados.get('titulo', tarefa.title)
    tarefa.description = dados.get('descricao', tarefa.description)
    tarefa.done = dados.get('concluida', tarefa.done)
    
    db.session.commit()
    
    return jsonify({'id': tarefa.id, 'titulo': tarefa.title, 'concluida': tarefa.done})

@api_bp.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    tarefa = Task.query.get_or_404(id)
    
    db.session.delete(tarefa)
    db.session.commit()
    
    return jsonify({'mensagem': f'Tarefa {id} removida com sucesso!'})