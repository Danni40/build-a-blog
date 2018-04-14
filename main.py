from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(380))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST', 'GET'])
def addPost():

    title_error=''
    body_error=''

    if request.method == 'POST':
        blog_name = request.form['blog']
        blog_body = request.form['body']

        if blog_name == '':
            title_error = "Please enter a blog title."
            return render_template("addPost.html", blog_name=blog_name, 
                blog_body=blog_body, title_error=title_error)
            
        if blog_body == '':
            body_error = "Please complete a blog entry."
            return render_template("addPost.html", blog_name=blog_name, 
                blog_body=blog_body, body_error=body_error)
        
        new_blog = Blog(blog_name, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()

    return render_template('addPost.html')

@app.route('/blog')
def blog():
    if not request.args:
        blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
        return render_template("blog.html", blogs = blogs)
    elif request.args.get('id'):
        user_id = request.args.get('id')
        blog = Blog.query.filter_by(id=user_id).first()
        return render_template('indiBlog.html', blog=blog)
        
@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()

    return render_template('blog.html', title="Build A Blog", blogs=blogs)

if __name__ == '__main__':
    app.run()