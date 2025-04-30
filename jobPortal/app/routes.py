
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from .models import User, Job, Application
from .forms import RegisterForm, LoginForm, JobForm

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def home():
    jobs = Job.query.all()
    return render_template('home.html', jobs=jobs)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_pw, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role == 'employer':
        form = JobForm()
        if form.validate_on_submit():
            job = Job(
                title=form.title.data,
                description=form.description.data,
                salary=form.salary.data,
                location=form.location.data,
                employer_id=current_user.id
            )
            db.session.add(job)
            db.session.commit()
            flash('Job posted successfully')
        jobs = Job.query.filter_by(employer_id=current_user.id).all()
        return render_template('employer_dashboard.html', form=form, jobs=jobs)
    else:
        jobs = Job.query.all()
        return render_template('jobseeker_dashboard.html', jobs=jobs)

@main.route('/apply/<int:job_id>')
@login_required
def apply(job_id):
    if current_user.role != 'jobseeker':
        flash('Only Job Seekers can apply.')
        return redirect(url_for('main.dashboard'))
    already_applied = Application.query.filter_by(job_id=job_id, user_id=current_user.id).first()
    if not already_applied:
        app = Application(job_id=job_id, user_id=current_user.id)
        db.session.add(app)
        db.session.commit()
        flash('Applied successfully')
    else:
        flash('Already applied for this job.')
    return redirect(url_for('main.dashboard'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
