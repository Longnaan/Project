from flask import Flask, render_template, request, redirect, url_for
from model import db, User, Assessment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyber_risk.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/assess', methods=['GET', 'POST'])
def assess():
    if request.method == 'POST':
        risk_level = request.form['risk_level']
        economic_impact = calculate_impact(risk_level)
        new_assessment = Assessment(risk_level=risk_level, economic_impact=economic_impact, user_id=1) # assuming user_id is 1 for simplicity
        db.session.add(new_assessment)
        db.session.commit()
        return render_template('result.html', risk_level=risk_level, economic_impact=economic_impact)
    return render_template('assess.html')

def calculate_impact(risk_level):
    # Simplified risk calculation
    risk_impact = {
        'low': 10000,
        'medium': 50000,
        'high': 100000
    }
    return risk_impact.get(risk_level.lower(), 0)

if __name__ == '__main__':
    app.run(debug=True)