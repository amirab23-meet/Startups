
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase 
import datetime


config = {
  "apiKey": "AIzaSyBwMLMG6TlrTRWvrImpn7kgKxVEF3ExJRI",
  "authDomain": "cs-amir-gp-f.firebaseapp.com",
  "projectId": "cs-amir-gp-f",
  "storageBucket": "cs-amir-gp-f.appspot.com",
  "messagingSenderId": "531475169244",
  "appId": "1:531475169244:web:06192ca20d569bc89a5919",
  "measurementId": "G-SL0HLVBCQG",
  "databaseURL":"https://cs-amir-gp-f-default-rtdb.europe-west1.firebasedatabase.app/"}




firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'trytoguessbish'




@app.route('/', methods=['GET', 'POST'])
def signin():
    error="failed"
    if request.method == "POST":
        login_session['email'] = request.form['email']
        login_session['password'] = request.form['password']
        try:
            login_session['user'] = user = auth.sign_in_with_email_and_password(login_session["email"], login_session["password"])
            return(redirect('design'))
        except:
            error="problem"
            return render_template("inerror.html")
            
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == "POST":
        login_session['email']= request.form['email']
        login_session['full_name']= request.form['full_name']
        login_session['username']= request.form['username']
        login_session['option']= request.form['option']
        login_session['password']= request.form['password']
        

        # try:
        login_session['user'] = auth.create_user_with_email_and_password(login_session["email"], request.form['password'])
        user= {"email": request.form['email'],"full_name": request.form['full_name'],"username": request.form['username'],"password": request.form['password'],"option": request.form['option'] }
        user = db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('design'))
        # except:
            # return render_template("signup.html", error="problem")
    else:
        return render_template("signup.html")


@app.route('/design')
def design():
    if login_session['user']:
        username = db.child("Users").child(login_session['user']['localId']).get().val()['username']
        option = db.child("Users").child(login_session['user']['localId']).get().val()['option']
        return render_template('design.html', username = username , option = option) 
    else:
        return redirect(url_for('signin'))


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/main')
def main():
    
    return render_template("main.html"   )


@app.route('/inerror')
def inerror():
    return render_template("inerror.html")

@app.route('/notes')
def notes():

    return render_template('notes.html')


'''@app.route('/posts')
def posts():

    return render_template('posts.html')    
'''
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    error=""
    if request.method == "POST":
        username = db.child("Users").child(login_session['user']['localId']).get().val()['username']
        title= request.form['title']
        description= request.form['description']
        now = datetime.datetime.now()

        current_time = now.strftime("%H:%M:%S")

        # try:
        post= {"username": username,"title": title,"description": description,"current_time": current_time }
        db.child("Posts").push(post)
        
        return redirect(url_for('posts'))
        # except:
            # return render_template("signup.html", error="problem")
    else:

        
        base = (db.child("Posts").get().val())
        
        if base == None:
            base= {'t':{'title' : 'FIRST POST EVER', 'current_time': 'The biginning of time', 'username':"Mysteryyyy", "description": "Never to be deleted"}}
        else:
            base['t'] = {'title' : 'FIRST POST EVER', 'current_time':'The biginning of time', 'username':"Mysteryyyy", "description": "Never to be deleted"}
        
        return render_template('posts.html', base=base)





if __name__ == '__main__':
    app.run(debug=True)