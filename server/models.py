from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

click_baity_list = ["Won't Believe", "Secret", "Top", "Guess"]

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name', 'phone_number')
    def validate_data(self, key, data):
        if key == 'name' and data == '':
            raise ValueError('Need a name')
        if key == 'phone_number' and len(data) != 10:
            raise ValueError('Wrong number of digits')
        return data

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, db.CheckConstraint('len(content) >= 250'))
    category = db.Column(db.String, db.CheckConstraint('(category == "Fiction") or (category == "Non-Fiction")'))
    summary = db.Column(db.String, db.CheckConstraint('len(summary) < 250'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content', 'summary', 'category', 'title')
    def validate_data(self, key, data):
        if key == 'content' and len(data) < 250:
            raise ValueError('Content is too short!')
        if key == 'summary' and len(data) >= 250:
            raise ValueError('Summary is too long!')
        if key == 'category' and data != 'Fiction' and data != 'Non-Fiction':
            raise ValueError('Not the correct category.')
        if key == 'title':
            no_bait = True
            for bait in click_baity_list:
                if bait in data:
                    no_bait = False
                    break
            if no_bait:
                raise ValueError('Need better title!')
        return data

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
