from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)
#Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Create a function to return a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id
subscribers = []
@app.route('/friends' , methods=['POST', 'GET'])
def friends():
    title = "Qeydiyyatdan kecenlerin siyahisi"
    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)
        #Push to Database
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding your.."
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", title=title, friends=friends)


@app.route('/')
def index():
    title = "John Elder's blog"
    return render_template("index.html", title=title)
@app.route('/about')
def about():
    title = "About John Elder!"
    names = ["John", "Marry", "Wes", "Sally"]
    return render_template("about.html", names=names, title=title)

@app.route('/subscribe')
def subscribe():
    title = "Subscribe To My Email Newsletter"
    return render_template("subscribe.html", title=title)
@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    if not first_name or not last_name or not email:
        error_statement = "All Form Fields Required..."
        return render_template("subscribe.html",
                    error_statement=error_statement,
                    first_name=first_name,
                    Last_name=last_name,
                    email=email)
    subscribers.append(f"{first_name} {last_name}|{email}")
    title = "Thank You!"
    return render_template("form.html", title=title, subscribers=subscribers)
    
if __name__=="__main__":
    app.run(debug=True)