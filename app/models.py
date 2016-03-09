from app import db,bcrypt
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property


class User(UserMixin, db.Model):
    __tablename__ = 'user'    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    jobposter=db.Column(db.Boolean, default=False)
    suggester=db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime)
    _password = db.Column(db.String(128))
    confirmed=db.Column(db.Boolean, default=False)
    paypalemail=db.Column(db.String(140), nullable=True)
    wins = db.Column(db.Integer, default=0)
    totalwinnings=db.Column(db.Float, default=0)
    emailnotes=db.Column(db.Boolean, default=True)
    postings = db.relationship('Posting', backref='creator', lazy='dynamic')
    
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = generate_password_hash(plaintext)
    
    def is_correct_password(self, plaintext):
        if bcrypt.check_password_hash(self._password, plaintext):
            return True
    
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.email)
    

class Posting(db.Model):
    __tablename__ = 'posting'   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    description = db.Column(db.String())
    anything_else = db.Column(db.String())
    timestamp = db.Column(db.DateTime)
    timestamp_day = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    suggestions = db.relationship('Suggestion', backref='poster', lazy='dynamic')
    status=   db.Column(db.String(140), default="Pending",nullable=True) 
    winner= db.Column(db.String(140), nullable=True) 
    project_type = db.Column(db.String(140)) 
    project_prize=db.Column(db.Float)
    number_of_entries=db.Column(db.Integer, default=0)
    
    
    def __repr__(self):
        return '<Post %r>' % (self.title)
        
class Suggestion(db.Model):
    __tablename__ = 'suggestion'   
    id = db.Column(db.Integer, primary_key=True)
    Suggest1 = db.Column(db.String(140))
    Suggest2 = db.Column(db.String(140))
    Suggest3 = db.Column(db.String(140))
    Suggest4 = db.Column(db.String(140))
    Suggest5 = db.Column(db.String(140))
    suggester=db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    timestamp_day = db.Column(db.Date)
    posting_id = db.Column(db.Integer, db.ForeignKey('posting.id'))
    winstatus=db.Column(db.Boolean, default=False) 

    def __repr__(self):
        return '<Suggestion: %r>' % (self.id)