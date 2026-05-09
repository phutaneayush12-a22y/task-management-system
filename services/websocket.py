from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio

class WebSocketService:
    
    @staticmethod
    @socketio.on('connect')
    def handle_connect():
        if current_user.is_authenticated:
            join_room(str(current_user.id))
            emit('connected', {'message': f'Connected to task updates for user {current_user.username}'})
    
    @staticmethod
    @socketio.on('disconnect')
    def handle_disconnect():
        if current_user.is_authenticated:
            leave_room(str(current_user.id))
    
    @staticmethod
    def send_task_update(action, task_data):
        """Send task update to specific user's room"""
        if 'user_id' in task_data:
            socketio.emit('task_update', {
                'action': action,
                'data': task_data
            }, room=str(task_data['user_id']))