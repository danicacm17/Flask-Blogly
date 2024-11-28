# Import necessary libraries and modules
from flask import Flask, request, redirect, render_template, flash, abort
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from models import db, connect_db, User, Post, Tag
from flask_caching import Cache
import pytz
from datetime import datetime

# Initialize the Flask app and configure settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = '965-416-415'

# Set up debug toolbar and other necessary extensions
toolbar = DebugToolbarExtension(app)
connect_db(app)
migrate = Migrate(app, db)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Error handling for 404 pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Route to render the homepage with the 5 most recent posts
@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

# Routes for user management
@app.route('/users')
def users_index():
    """Display a list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Display a form to create a new user"""
    return render_template('users/new.html')

@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    # Validation for required fields
    if not first_name or not last_name:
        flash("First Name and Last Name are required.", "danger")
        return redirect("/users/new")

    # Create and save new user
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    flash("User created successfully!", "success")
    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show detailed info for a specific user and their posts"""
    user = User.query.get_or_404(user_id)
    est = pytz.timezone('US/Eastern')
    for post in user.posts:
        if post.created_at:
            post.created_at = post.created_at.astimezone(est)
    return render_template('users/show.html', user=user, posts=user.posts)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit user details"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle deletion of a user and their posts"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User and associated posts deleted successfully!', 'success')
    return redirect("/users")

# Routes for post management
@app.route('/posts')
@cache.cached(timeout=60)
def posts():
    """Display all posts"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts/all_posts.html', posts=posts)

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    """Create a new post for a specific user"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Title and content are required!', 'danger')
            return redirect(f'/users/{user.id}/posts/new')

        new_post = Post(title=title, content=content, user_id=user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(f'/users/{user.id}')

    return render_template('posts/new_post.html', user=user)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()  # Fetch all available tags
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']

        # Handle the tags
        selected_tags = request.form.getlist('tags')  # Get list of selected tag IDs
        post.tags = []  # Clear current tags
        for tag_id in selected_tags:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)  # Associate selected tags with post

        db.session.commit()
        flash("Post updated successfully!")
        return redirect(f'/posts/{post.id}')

    return render_template('posts/edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete an existing post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    """Show the details of a specific post"""
    # Retrieve the post from the database
    post = Post.query.get_or_404(post_id)

    # Convert the created_at field to EST
    est = pytz.timezone('US/Eastern')

    # Check if created_at exists and convert it to the EST timezone
    if post.created_at:
        post.created_at = post.created_at.astimezone(est)

    # Format the time in EST
    formatted_time = post.created_at.strftime('%b %d, %Y at %I:%M %p')

    # Render the template and pass the formatted time
    return render_template('posts/post_detail.html', post=post, formatted_time=formatted_time)

@app.route('/tags')
def list_tags():
    """Show a list of all tags."""
    tags = Tag.query.all()  # Fetch all tags from the database
    return render_template('tags/tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_detail.html', tag=tag)

@app.route('/tags/new', methods=["GET", "POST"])
def new_tag():
    """Handle creating a new tag."""
    if request.method == 'POST':
        tag_name = request.form['name']
        
        # Validate the tag name
        if not tag_name:
            flash("Tag name is required.", "danger")
            return redirect('/tags/new')
        
        # Check if the tag already exists
        existing_tag = Tag.query.filter_by(name=tag_name).first()
        if existing_tag:
            flash("Tag already exists.", "danger")
            return redirect('/tags/new')

        # Create and save the new tag
        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        flash("Tag created successfully!", "success")
        return redirect('/tags')
    
    return render_template('tags/new_tag.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
