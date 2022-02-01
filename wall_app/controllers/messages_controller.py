from flask import redirect, render_template, request, session
from wall_app import app
from wall_app.models.message_model import Message
from flask import request
from flask import jsonify

@app.route("/send-message",methods=['POST'])
def send_message():
    data = {
        'message':request.form['message'],
        'user_id':request.form['user_id'],
        'recipient_id':request.form['receiver']
    }
    response_query_create = Message.create_new_message(data)
    return redirect("/result")

@app.route("/delete/<int:id>",methods=['GET'])
def delete_message(id):
    if 'id' not in session:
        return redirect('/logout')
    data_id={
        "id":session['id']
    }
    if not Message.validate_delete_message(data_id,id):
        return redirect("/danger")
    data = {
        'id':id
    }
    print("aqui id para eliminar",id)
    print(Message.delete_message(data))    
    return redirect("/result")
@app.route("/danger",methods=['GET'])
def danger_message():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip=request.environ['REMOTE_ADDR']
    else:
        ip= request.environ['HTTP_X_FORWARDED_FOR'] 
    return render_template("danger.html",ip=ip)