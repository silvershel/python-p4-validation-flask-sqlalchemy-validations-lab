from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name', 'phone_number')
    def validate_author(self, key, value):
        if key == 'name':
            existing_author = Author.query.filter(Author.name == value).first()
            if existing_author:
                raise ValueError("Author name must be unique.")
            if not value:
                raise ValueError("Author must have a name.")
        elif key == 'phone_number':
            if len(value) != 10 or not value.isdigit():
                raise ValueError("requires each phone number to be exactly ten digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('content', 'category', 'summary', 'title')
    def validate_content(self, key, value):
        if key == 'content':
            if len(value) < 250:
                raise ValueError("Content must be at least 250 characters.")
        elif key == 'category':
            if value not in ["Fiction", "Non-Fiction"]:
                raise ValueError("Category must be 'Fiction' or 'Non-Fiction'.")
        elif key == 'summary':
            if len(value) > 250:
                raise ValueError("Post summary must be a max of 250 characters.")
        elif key == 'title':
            found_phrase = False
            for phrase in ["Won't Believe", "Secret", "Top", "Guess"]:
                if phrase in value:
                    found_phrase = True
                    break
            if not found_phrase:
                raise ValueError("Post title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
