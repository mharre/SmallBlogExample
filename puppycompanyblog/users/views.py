from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from puppycompanyblog import db
from werkzeug.security import generate_password_hash,check_password_hash
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm() #instance of the form we created

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        #if validated on submit we create our user based on info provided

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!') #pointless flash, too quick
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

# login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()


        if user.check_password(form.password.data) and user is not None:
            #check_password method we created from our main models.py
            login_user(user)
            flash('Logged in successfully.')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
            #if next==none means they went straight to login page
            #not next[0]=='/' means: or wasn't equal to the homepage
                next = url_for('core.index')
                #set next to the home page and then redirect them to next, 
                #OR let them go to the page they were trying to view: request.args etc
            return redirect(next)
    return render_template('login.html', form=form)



# logout
@users.route("/logout")
def logout():
    logout_user() #import from flask_login
    return redirect(url_for('core.index'))

# account (update UserForm)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
        #if they uploaded picture data
            username = current_user.username
            #taking current username if they uploaded a picture
            pic = add_profile_pic(form.picture.data,username)
            #taking the picture data and their username and passing it to the func we created
            current_user.profile_image = pic
            #in our User model they have profile_img which is just a string of the filename

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        #this means they are not submitting anything so we just want their current info

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    #default image unless they have updated it
    return render_template('account.html', profile_image=profile_image, form=form)

# user's list of Blog posts
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    #allows us to cycle through users posts with pages
    user = User.query.filter_by(username=username).first_or_404()
    #this is if someone tries to type a username page in directly but mispells, it will display
    #our 404 page. either correct page or 404
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
