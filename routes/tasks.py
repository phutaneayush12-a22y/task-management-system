from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from socketio_instance import socketio
from models.task import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
@login_required
def get_tasks():
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
        return jsonify({'tasks': [task.to_dict() for task in tasks]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/', methods=['POST'])
@login_required
def add_task():
    try:
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'Medium'),
            status=data.get('status', 'Pending'),
            user_id=current_user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Emit WebSocket event
        socketio.emit('task_updated', {
            'action': 'add',
            'task': task.to_dict()
        }, room=str(current_user.id))
        
        return jsonify({'message': 'Task added successfully', 'task': task.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            task.priority = data['priority']
        if 'status' in data:
            task.status = data['status']
        
        db.session.commit()
        
        # Emit WebSocket event
        socketio.emit('task_updated', {
            'action': 'update',
            'task': task.to_dict()
        }, room=str(current_user.id))
        
        return jsonify({'message': 'Task updated successfully', 'task': task.to_dict()}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        # Emit WebSocket event
        socketio.emit('task_updated', {
            'action': 'delete',
            'task_id': task_id
        }, room=str(current_user.id))
        
        return jsonify({'message': 'Task deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500