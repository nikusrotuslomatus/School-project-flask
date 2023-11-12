from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

spisok = ""
spisok+= "Home_of_Akame1 "
spisok+="Next_time_line2 "
spisok+= "Chin-chopa3 "

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    img = db.Column(db.String(4000), default="https://w-dog.ru/wallpapers/16/8/474556596967390/volchica-i-pryanosti-xolo-xoro-doma.jpg")
    buttons = db.Column(db.String(400), default= "Home_of_Akame1 " + "Next_time_line2 " + "Chin-chopa3 ")
    name = db.Column(db.String(400))
    def __repr__(self):
        return '<Task %r>' % self.id


import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/', methods=['GET'])
def sharlotta():
    global spisok
    page = Todo.query.get_or_404(1)
    all_buttons = page.buttons.split()
    return render_template("Starting.html", page = page, buttons = all_buttons)
"""
@app.route('/', methods=['GET'])
def Start():
    location1 = Todo(description = "Welcome to akamochka", img="https://klike.net/uploads/posts/2019-10/1572076136_8.jpg", name="Home of Akame")
    location2 = Todo(description="Welcome to Gates of Steins", img="https://moe.shikimori.one/system/user_images/original/115801/442797.jpg", name="Next time line")
    location3 = Todo(description="Welcome to Fresh meat zone", img="https://i.ytimg.com/vi/xAYVsN_rXtU/maxresdefault.jpg", name="Chin-chopa")
    try:
        db.session.add(location1)
        db.session.add(location2)
        db.session.add(location3)
        db.session.commit()
        return redirect('/room/<int:1>')

    except Exception as e:
        print(e)
    return render_template("test.html")
"""
@app.route('/room/<int:id>', methods=['GET'])
def room(id):

    page = Todo.query.get_or_404(id)
    all_buttons = page.buttons.split()

    return render_template('Starting.html', page = page, buttons = all_buttons)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    global spisok

    if request.method == 'POST':
        user_info = request.form['content'].split()
        location4 = Todo(description=user_info[1], img=user_info[2], name=user_info[0])
        spisok+=str(user_info[0]) + str(len(spisok.split()) + 1) + " "

        try:
            db.session.add(location4)
            db.session.commit()
        except:

            pass
        pages = Todo.query.order_by(Todo.date_created).all()
        for page in pages:
            page.buttons=spisok
            try:
                db.session.commit()
            except:
                pass
        return redirect('/room/' + str(id))
    else:
        page = Todo.query.get_or_404(id)
        return render_template('update.html', page = page)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port="8888")