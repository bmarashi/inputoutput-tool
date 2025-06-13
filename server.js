const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static('public'));

// Store posts in a JSON file
const POSTS_FILE = path.join(__dirname, 'posts.json');

// Initialize posts file if it doesn't exist
if (!fs.existsSync(POSTS_FILE)) {
    fs.writeFileSync(POSTS_FILE, JSON.stringify([]));
}

// Get all posts
app.get('/api/posts', (req, res) => {
    const posts = JSON.parse(fs.readFileSync(POSTS_FILE));
    res.json(posts);
});

// Add a new post
app.post('/api/posts', (req, res) => {
    const { title, content } = req.body;
    
    if (!title || !content) {
        return res.status(400).json({ error: 'Title and content are required' });
    }

    const posts = JSON.parse(fs.readFileSync(POSTS_FILE));
    const newPost = {
        id: Date.now(),
        title,
        content,
        date: new Date().toLocaleDateString()
    };

    posts.unshift(newPost);
    posts.splice(10); // Keep only last 10 posts
    fs.writeFileSync(POSTS_FILE, JSON.stringify(posts));

    res.status(201).json(newPost);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
