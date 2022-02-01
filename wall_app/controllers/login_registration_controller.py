from flask import flash, redirect, render_template, request, session
from wall_app import app,bcrypt
from wall_app.models.message_model import Message
from wall_app.models.user_model import User


@app.route("/" , methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/register",methods=['POST'])
def registration():
    if not User.validate_registration(request.form):
            return redirect("/")
        
    password_encriptado = bcrypt.generate_password_hash(request.form['password1'])
    data = {
        'first_name':request.form['firstname'],
        'last_name':request.form['lastname'],
        'email':request.form['email'],
        'password':password_encriptado
    }
    response_query = User.create_user(data)
    session['id'] = response_query
    return redirect("/result")

@app.route("/login",methods=['POST'])
def login():
    response_query_user=User.get_user_by_email(request.form)
    
    if not response_query_user:
        flash("El correo no existe","login")
        return redirect('/')
    
    if not bcrypt.check_password_hash( response_query_user.password, request.form['password']):
        flash("el password no es correcto","login")
        return redirect("/")
    session['id'] = response_query_user.id
    return redirect("/result")

@app.route("/result",methods=['GET'])
def result_user():
    if 'id' not in session:
        return redirect('/logout')
    data ={
        'id': session['id']
    }
    response_query_user=User.get_user_by_id(data)
    response_query_users_except=User.get_all_users_except(data)
    response_query_messages_received = Message.get_all_received_messages(data)
    return render_template("result.html",user=response_query_user,user_receivers=response_query_users_except,senders=response_query_messages_received)

@app.route("/logout",methods=['GET'])
def logout():
    session.clear()
    return redirect("/")