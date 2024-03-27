from flask import Flask, render_template, request, send_from_directory
import pymysql as sql

app = Flask(__name__)

def db_connect():
    db = sql.connect(host='localhost', user='root', password='', port=3306, database='python8am')
    cur = db.cursor()
    return db, cur

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/portfolio/')
def portfolio():
    return render_template('portfolio.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/aftersubmit/', methods=['GET', 'POST'])
def aftersubmit():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        db, cur = db_connect()
        data = cur.execute(f"select * from portfolio where email='{email}'")
        if data:
            msg = 'Email already exists...'
            return render_template('contact.html', data=msg)
        else:
            db, cur = db_connect()
            cmd = f"insert into portfolio values('{name}', '{email}', '{phone}', '{message}')"
            cur.execute(cmd)
            db.commit()
            db.close()
            msg = 'Details are send successfully...'
            return render_template('contact.html', data=msg)

@app.route('/resume/')
def resume():
    return send_from_directory('static', 'Aditi_Garg_Resume.pdf')

app.run(host='localhost', port=5000, debug=True)