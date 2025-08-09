from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_student = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClickEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for anonymous users
    session_id = db.Column(db.String(100), nullable=False)
    page_url = db.Column(db.String(500), nullable=False)
    element_id = db.Column(db.String(200), nullable=True)
    element_class = db.Column(db.String(200), nullable=True)
    element_text = db.Column(db.String(500), nullable=True)
    click_x = db.Column(db.Integer, nullable=True)
    click_y = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    lectures = Lecture.query.filter_by(course_id=course_id).all()
    notes = Note.query.filter_by(course_id=course_id).all()
    return render_template('course_detail.html', course=course, lectures=lectures, notes=notes)

@app.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    if not current_user.is_student:  # Only instructors can create courses
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            
            course = Course(
                title=title,
                description=description,
                instructor_id=current_user.id
            )
            db.session.add(course)
            db.session.commit()
            
            flash('Course created successfully!', 'success')
            return redirect(url_for('course_detail', course_id=course.id))
        
        return render_template('create_course.html')
    else:
        flash('Students cannot create courses', 'error')
        return redirect(url_for('index'))

# Clickstream tracking routes
@app.route('/track_click', methods=['POST'])
def track_click():
    """Track user click events"""
    try:
        data = request.get_json()
        
        # Create click event
        click_event = ClickEvent(
            user_id=current_user.id if current_user.is_authenticated else None,
            session_id=session.get('session_id', 'anonymous'),
            page_url=data.get('page_url', ''),
            element_id=data.get('element_id', ''),
            element_class=data.get('element_class', ''),
            element_text=data.get('element_text', ''),
            click_x=data.get('click_x'),
            click_y=data.get('click_y'),
            user_agent=request.headers.get('User-Agent', ''),
            ip_address=request.remote_addr
        )
        
        db.session.add(click_event)
        db.session.commit()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/export_clickstream')
@login_required
def export_clickstream():
    """Export clickstream data to Excel"""
    try:
        # Get all click events
        click_events = ClickEvent.query.all()
        
        # Convert to DataFrame
        data = []
        for event in click_events:
            user = User.query.get(event.user_id) if event.user_id else None
            data.append({
                'ID': event.id,
                'User ID': event.user_id,
                'Username': user.username if user else 'Anonymous',
                'Session ID': event.session_id,
                'Page URL': event.page_url,
                'Element ID': event.element_id,
                'Element Class': event.element_class,
                'Element Text': event.element_text,
                'Click X': event.click_x,
                'Click Y': event.click_y,
                'Timestamp': event.timestamp,
                'User Agent': event.user_agent,
                'IP Address': event.ip_address
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Clickstream Data', index=False)
        
        output.seek(0)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'clickstream_data_{timestamp}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        flash(f'Error exporting data: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/export_data')
@login_required
def export_data():
    """Simple export page for clickstream data"""
    return render_template('export_data.html')

@app.route('/video_lectures')
@login_required
def video_lectures():
    """Video lectures page with embedded YouTube videos"""
    return render_template('video_lectures.html')

@app.route('/text_lessons')
@login_required
def text_lessons():
    """Text-based lessons page with high school math topics"""
    return render_template('text_lessons.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
