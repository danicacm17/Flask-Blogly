# import pytest
# from app import app, db, User, Post

# # Set up test client
# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///test_blogly"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     with app.test_client() as client:
#         yield client

#     # Clean up after each test
#     with app.app_context():
#         db.drop_all()
#         db.create_all()


# # Create a test user
# @pytest.fixture
# def new_user(client):
#     user = User(
#         first_name='John',
#         last_name='Doe',
#         image_url='http://example.com/image.jpg'
#     )
#     db.session.add(user)
#     db.session.commit()
#     return user


# # Create a test post
# @pytest.fixture
# def new_post(client, new_user):
#     post = Post(
#         title='Test Post',
#         content='This is a test post.',
#         user_id=new_user.id
#     )
#     db.session.add(post)
#     db.session.commit()
#     return post


# # Test User Creation (Redirects and Data Validation)
# def test_user_creation_redirect(client):
#     response = client.post('/users/new', data={
#         'first_name': 'Jane',
#         'last_name': 'Smith',
#         'image_url': 'http://example.com/image.jpg'
#     }, follow_redirects=True)

#     # Check if the user was redirected to the users' list page
#     assert response.request.path == '/users'

#     # Also check if the created user appears in the users list
#     assert b'Jane Smith' in response.data


# # Test Create Post (Flash Message and Redirect)
# def test_create_post(client, new_user):
#     response = client.post(f'/users/{new_user.id}/posts/new', data={
#         'title': 'Test Post',
#         'content': 'This is a test post.'
#     }, follow_redirects=True)

#     # Check if the flash message appears
#     assert b'Post created successfully!' in response.data

#     # Check if the user is redirected to their page
#     assert f'/users/{new_user.id}' in response.request.path


# # Test Flash Message on Missing Post Fields
# def test_flash_message_on_missing_post_fields(client, new_user):
#     response = client.post(f'/users/{new_user.id}/posts/new', data={
#         'title': '',
#         'content': ''
#     }, follow_redirects=True)

#     # Check if the error message is flashed
#     assert b'Title and content are required!' in response.data


# # Test Edit Post (Flash Message and Post Update)
# def test_edit_post(client, new_post):
#     response = client.post(f'/posts/{new_post.id}/edit', data={
#         'title': 'Updated Title',
#         'content': 'Updated content for the post.'
#     }, follow_redirects=True)

#     # Check if the flash message appears
#     assert b'Post updated successfully!' in response.data

#     # Check if the post's title and content were updated
#     assert b'Updated Title' in response.data
#     assert b'Updated content for the post.' in response.data


# # Test Post Deletion (Flash Message and Redirect)
# def test_delete_post(client, new_post):
#     response = client.post(f'/posts/{new_post.id}/delete', follow_redirects=True)

#     # Check if the flash message appears
#     assert b'Post deleted successfully!' in response.data

#     # Check if we are redirected to the user's page
#     assert f'/users/{new_post.user_id}' in response.request.path


# # Test that the users index page loads
# def test_users_index(client):
#     response = client.get('/users')
#     assert response.status_code == 200
#     assert b'Users' in response.data


# # Test that the new user form page loads
# def test_users_new_form(client):
#     response = client.get('/users/new')
#     assert response.status_code == 200
#     assert b'Create a user' in response.data


# # Test that the user details page loads
# def test_users_show(client, new_user):
#     response = client.get(f'/users/{new_user.id}')
#     assert response.status_code == 200
#     assert b'John Doe' in response.data


# # Test that the post detail page loads
# def test_post_detail_page(client, new_post):
#     response = client.get(f'/posts/{new_post.id}')
#     assert response.status_code == 200
#     assert b'Test Post' in response.data


# # Test that the new post form page loads
# def test_new_post_page(client, new_user):
#     response = client.get(f'/users/{new_user.id}/posts/new')
#     assert response.status_code == 200
#     assert b'Create a Post' in response.data
