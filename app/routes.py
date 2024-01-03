from flask import request
from app import app
from fake_data import post_data

@app.route('/')
def index():
    return 'Hello World'

# Get All Posts
@app.route('/posts')
def get_posts():
    posts = post_data
    return posts

# Get Post By ID
@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # Get the post based on the post id
    posts = post_data
    for post in posts:
        if post['id'] == post_id:
            return post
    return {'error': f'Post with {post_id} does not exist'}, 404

# Create New Post
@app.route('/posts', methods=['POST'])
def create_post():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    # Get data from the body
    title = data.get('title')
    body = data.get('body')
    
    # Create a new post
    new_post = {
        "id": len(post_data) + 1,
        "title": title,
        "body": body,
        "userId": 1,
        "dateCreated": "2024-01-10T12:30:45",
        "likes": 0,
    }
    post_data.append(new_post)
    return new_post, 201
