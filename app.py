from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamesphere.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('class_selection'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/class_selection')
@login_required
def class_selection():
    return render_template('class_selection.html')

@app.route('/subject_selection/<class_name>')
@login_required
def subject_selection(class_name):
    return render_template('subject_selection.html', class_name=class_name)

@app.route('/notes/<class_name>/<subject>')
@login_required
def notes(class_name, subject):
    # This is a placeholder for the actual notes content
    notes_content = {
        'physics': {
            '8': 'Class 8 Physics Notes: Basic concepts of motion, force, and energy...',
            '9': 'Class 9 Physics Notes: Newton\'s laws, work, and energy...',
            '10': 'Class 10 Physics Notes: Electricity, magnetism, and modern physics...'
        },
        'chemistry': {
            '8': 'Class 8 Chemistry Notes: Basic elements, compounds, and mixtures...',
            '9': 'Class 9 Chemistry Notes: Atomic structure, periodic table...',
            '10': 'Class 10 Chemistry Notes: Chemical reactions, acids, and bases...'
        },
        'maths': {
            '8': 'Class 8 Maths Notes: Basic algebra, geometry, and statistics...',
            '9': 'Class 9 Maths Notes: Linear equations, polynomials...',
            '10': 'Class 10 Maths Notes: Quadratic equations, trigonometry...'
        }
    }
    
    return render_template('notes.html', 
                         class_name=class_name, 
                         subject=subject,
                         content=notes_content[subject][class_name])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 