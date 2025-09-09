from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default='Marketing Strategist')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Progress tracking
    current_track = db.Column(db.Integer, default=1)
    current_module = db.Column(db.Integer, default=1)
    completed_modules = db.Column(db.Text, default='[]')  # JSON array of completed module IDs
    certifications = db.Column(db.Text, default='[]')  # JSON array of earned certification IDs
    
    def get_completed_modules(self):
        return json.loads(self.completed_modules) if self.completed_modules else []
    
    def set_completed_modules(self, modules):
        self.completed_modules = json.dumps(modules)
    
    def get_certifications(self):
        return json.loads(self.certifications) if self.certifications else []
    
    def set_certifications(self, certs):
        self.certifications = json.dumps(certs)

class ModuleProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    track_id = db.Column(db.Integer, nullable=False)
    module_id = db.Column(db.Integer, nullable=False)
    completed_sections = db.Column(db.Text, default='[]')  # JSON array of completed section IDs
    notes = db.Column(db.Text, default='')
    exercise_responses = db.Column(db.Text, default='{}')  # JSON object of exercise responses
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_completed_sections(self):
        return json.loads(self.completed_sections) if self.completed_sections else []
    
    def set_completed_sections(self, sections):
        self.completed_sections = json.dumps(sections)
    
    def get_exercise_responses(self):
        return json.loads(self.exercise_responses) if self.exercise_responses else {}
    
    def set_exercise_responses(self, responses):
        self.exercise_responses = json.dumps(responses)

class CertificationAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    track_id = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON object of question_id: answer_index
    score = db.Column(db.Float, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)  # seconds
    attempt_number = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_answers(self):
        return json.loads(self.answers) if self.answers else {}
    
    def set_answers(self, answers):
        self.answers = json.dumps(answers)

class LearningActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'module', 'track', 'certification', 'enrollment'
    description = db.Column(db.String(200), nullable=False)
    track_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

