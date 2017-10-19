from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:12345@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'iwillnevertell'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    new_post = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, new_post, owner):
        self.title = title
        self.new_post = new_post
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            #i will need to validate here
            return redirect('/login.html')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if password != verify:
            flash('Passwords do not match!')
            return redirect('/signup')

        if not username or not password or not verify:
            flash('You left a text box blank!')
            return redirect('/signup')

        if len(username) < 3:
            flash('Use your imagination; username is too short!')
            return redirect('/signup')

        if len(password) < 3:
            flash('Do you want to be hacked? Make a longer password!')
            return redirect('/signup')

        existing_username = User.query.filter_by(username=username).first()
        if not existing_username:
            new_username = User(username, password)
            db.session.add(new_username)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            flash('That username already exists!')
            return redirect('/signup')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/')
def index():
    usernames = User.query.all()
    return render_template('index.html', usernames=usernames)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method=="POST":
        title = request.form['title']
        new_post = request.form['new_post']
        owner = User.query.filter_by(username=session['username']).first()
        
        if not title and not new_post:
            flash("You didn't write anything, boooooooring!")
            return redirect('/newpost')
        
        if not title:
            flash("You left the title empty, you big goon!")
            return redirect('/newpost')
        if not new_post:
            flash("Whoops! You left the textbox blank!")
            return redirect('/newpost')
      
        else:
            new_blog = Blog(title, new_post, owner) 
            db.session.add(new_blog)
            db.session.commit()
            
            #blog_id = str(new_blog.blog_id)
            #return redirect('/blog?id='+ blog_id)
            return redirect('/blog?id=' + str(new_blog.id))
    
    
    #blogs = Blog.query.filter_by(completed=False,owner=owner).all()
    #completed_blogs = Blog.query.filter_by(completed=True, owner=owner).all()
    return render_template('newpost.html', title="Add a Blog Entry")                  

@app.route('/blog', methods=['GET'])
def all_blog_posts():

    if request.method == "GET" and "id" in request.args:
        id = request.args.get("id")
        blog = Blog.query.filter_by(id=id).first()
        owner_id = blog.owner
        #username = User.query.get(owner_id)
        return render_template('uniqueblog.html', title="Build a Blog", blog=blog, owner_id=owner_id)
    
    if request.method == "GET" and "username" in request.args:
        username = request.args.get("username")
        user_id = User.query.filter_by(username=username).first()
        user_posts = Blog.query.filter_by(owner=user_id).all()
        return render_template("singleUser.html", title=username + "'s" + " Posts", 
    user_posts=user_posts, username=username, user_id=user_id)
    else:
        blogs = Blog.query.all()
        
        return render_template('blog.html', blogs=blogs)



if __name__ == '__main__':
    app.run()