from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models.task import Task
import pandas as pd
import numpy as np

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard', methods=['GET'])
@login_required
def get_analytics():
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        
        if not tasks:
            return jsonify({
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'completion_percentage': 0,
                'priority_breakdown': {},
                'status_breakdown': {}
            }), 200
        
        tasks_data = [{
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'status': task.status,
            'created_at': task.created_at
        } for task in tasks]
        
        df = pd.DataFrame(tasks_data)
        
        total_tasks = len(df)
        completed_tasks = len(df[df['status'] == 'Completed'])
        pending_tasks = total_tasks - completed_tasks
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        priority_breakdown = df['priority'].value_counts().to_dict()
        status_breakdown = df['status'].value_counts().to_dict()
        
        return jsonify({
            'total_tasks': int(total_tasks),
            'completed_tasks': int(completed_tasks),
            'pending_tasks': int(pending_tasks),
            'completion_percentage': float(completion_percentage),
            'priority_breakdown': priority_breakdown,
            'status_breakdown': status_breakdown
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500