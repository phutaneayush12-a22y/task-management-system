from models.task import Task
from app import db
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.tasks = Task.query.filter_by(user_id=user_id).all()
        self.df = self._create_dataframe()
    
    def _create_dataframe(self):
        if not self.tasks:
            return pd.DataFrame()
        
        data = [{
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'status': task.status,
            'created_at': task.created_at,
            'updated_at': task.updated_at
        } for task in self.tasks]
        
        df = pd.DataFrame(data)
        
        # Add computed columns
        priority_map = {'Low': 1, 'Medium': 2, 'High': 3}
        df['priority_score'] = df['priority'].map(priority_map)
        df['is_completed'] = (df['status'] == 'Completed').astype(int)
        
        return df
    
    def get_summary_stats(self):
        if self.df.empty:
            return {
                'total': 0,
                'completed': 0,
                'pending': 0,
                'completion_rate': 0,
                'avg_priority': 0,
                'tasks_by_priority': {},
                'tasks_by_status': {}
            }
        
        total = len(self.df)
        completed = len(self.df[self.df['status'] == 'Completed'])
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            'total': int(total),
            'completed': int(completed),
            'pending': int(pending),
            'completion_rate': float(completion_rate),
            'avg_priority': float(self.df['priority_score'].mean()) if not self.df.empty else 0,
            'tasks_by_priority': self.df['priority'].value_counts().to_dict(),
            'tasks_by_status': self.df['status'].value_counts().to_dict()
        }
    
    def get_time_series_data(self, days=7):
        if self.df.empty:
            return []
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        filtered_df = self.df[self.df['created_at'] >= cutoff_date]
        
        time_series = filtered_df.groupby(filtered_df['created_at'].dt.date).size()
        
        return [{'date': str(date), 'count': int(count)} for date, count in time_series.items()]