"""SQLAlchemy models for blogly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Default image URL used for users who don't have a profile image
DEFAULT_IMAGE_URL = "https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg"

# User model, representing a user in the system
class User(db.Model):
    __tablename__ = 'users'

    # Columns for user attributes
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user
    first_name = db.Column(db.String(50), nullable=False)  # First name, required
    last_name = db.Column(db.String(50), nullable=False)  # Last name, required
    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_IMAGE_URL)  # Set default image URL

    # One-to-many relationship: a user can have many posts
    posts = db.relationship('Post', backref='author', cascade='all, delete-orphan')

    # Property to return the full name of the user by combining first and last name
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Post model, representing a blog post written by a user
class Post(db.Model):
    __tablename__ = 'posts'

    # Columns for post attributes
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the post
    title = db.Column(db.String(100), nullable=False)  # Post title, required
    content = db.Column(db.Text, nullable=False)  # Post content, required
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the post is created
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking the post to a user

    # One-to-many relationship: a post belongs to one user
    user = db.relationship('User', backref='user_posts')

# Tag model, representing a tag for categorizing posts
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the tag
    name = db.Column(db.String(50), unique=True, nullable=False)  # Tag name, required and unique

    # Many-to-many relationship: tags associated with posts
    posts = db.relationship('Post', secondary='post_tags', backref='tags')

# PostTag model, representing the association table for Post and Tag
class PostTag(db.Model):
    __tablename__ = 'post_tags'

    # Composite primary key using `post_id` and `tag_id`
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)  # Foreign key to Post
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)  # Foreign key to Tag

# Function to connect the database to the provided Flask app
def connect_db(app):
    """Connect this database to the provided Flask app.

    You should call this function in your Flask app to initialize the connection.
    """
    db.app = app  # Associate the app with the database
    db.init_app(app)  # Initialize the database with the app
