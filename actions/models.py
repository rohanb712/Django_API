import json
import os
from datetime import date
from django.conf import settings

class ActionManager:
    def __init__(self):
        self.file_path = os.path.join(settings.BASE_DIR, 'actions_data.json')
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def _load_actions(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_actions(self, actions):
        with open(self.file_path, 'w') as f:
            json.dump(actions, f, indent=2, default=str)
    
    def _get_next_id(self, actions):
        if not actions:
            return 1
        return max(action['id'] for action in actions) + 1
    
    def get_all(self):
        return self._load_actions()
    
    def get_by_id(self, action_id):
        actions = self._load_actions()
        for action in actions:
            if action['id'] == action_id:
                return action
        return None
    
    def create(self, action_data):
        actions = self._load_actions()
        action_data['id'] = self._get_next_id(actions)
        actions.append(action_data)
        self._save_actions(actions)
        return action_data
    
    def update(self, action_id, action_data):
        actions = self._load_actions()
        for i, action in enumerate(actions):
            if action['id'] == action_id:
                action_data['id'] = action_id
                actions[i] = action_data
                self._save_actions(actions)
                return action_data
        return None
    
    def delete(self, action_id):
        actions = self._load_actions()
        actions = [action for action in actions if action['id'] != action_id]
        self._save_actions(actions)
        return True

class Action:
    def __init__(self, id=None, action=None, date=None, points=None):
        self.id = id
        self.action = action
        self.date = date
        self.points = points
        self.objects = ActionManager()
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'date': self.date,
            'points': self.points
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            action=data.get('action'),
            date=data.get('date'),
            points=data.get('points')
        )
