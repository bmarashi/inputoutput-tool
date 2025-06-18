from flask import Flask, request, jsonify, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(port=5001, debug=True)

# Ensure posts.json exists
POSTS_FILE = 'posts.json'
if not os.path.exists(POSTS_FILE):
    with open(POSTS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    with open(POSTS_FILE, 'r') as f:
        posts = json.load(f)
    return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    with open(POSTS_FILE, 'r') as f:
        posts = json.load(f)

    new_post = {
        'id': datetime.now().timestamp(),
        'title': title,
        'content': content,
        'date': datetime.now().strftime('%B %d, %Y')
    }

    posts.insert(0, new_post)
    posts = posts[:10]  # Keep only last 10 posts

    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f)

    return jsonify(new_post), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
