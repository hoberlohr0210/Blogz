from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'iwillnevertell'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    new_post = db.Column(db.String(1000))
    #completed = db.Column(db.Boolean)
    #owner_id = db.Column(db.Integer)

    def __init__(self, title, new_post):
        self.title = title
        self.new_post = new_post
        #self.completed = False
        #self.owner = owner


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():


    if request.method == 'POST':
        title = request.form['title']
        new_post = request.form['new_post']
        #new_blog = (title, new_post)

        #blog = Blog.query.get(new_blog)

        if not title or not new_post:
            flash("You left a box empty, you big goon!")
            return redirect('/newpost')
        

        else:
             new_blog = Blog(title, new_post) 
             db.session.add(new_blog)
             db.session.commit()
             return redirect('/blog')
                

        # if len(title) < 3:
        #     flash("Use your imagination and write a longer title!")
        #     return redirect('/newpost')

        # if len(new_post) < 20:
        #     flash("Your life cannot possibly be that boring. Write a longer post!")
        #     return redirect('/newpost')

        # existing_blog = Blog.query.filter_by(new_post=new_post).first() 
        # if not existing_blog:
        #     new_blog = Blog(title, new_post) 
        #     db.session.add(new_blog)
        #     db.session.commit()
        #     return redirect('/blog')
        # else:
        #     flash('Whoops! Tell me something new, you already wrote that!')
        #     return redirect('/newpost')

       

    return render_template('newpost.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run()