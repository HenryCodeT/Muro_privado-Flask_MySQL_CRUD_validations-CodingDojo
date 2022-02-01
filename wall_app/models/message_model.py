from pyexpat.errors import messages
from wall_app.config.mysqlconnection import connectToMySQL
from wall_app.models import user_model
import math
from datetime import datetime
class Message:
    def __init__(self,data):
        self.id=data['id']
        self.message=data['message']
        self.user_id=data['user_id']
        self.recipient_id=data['recipient_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod 
    def create_new_message(cls,data):
        query=  '''
                INSERT INTO messages (message,user_id,recipient_id)
                VALUES (%(message)s,%(user_id)s,%(recipient_id)s);
                '''
        response_query = connectToMySQL('wall_db').query_db(query,data) 
        return response_query

    @classmethod 
    def delete_message(cls,data):
        query=  '''
                DELETE FROM messages WHERE id = %(id)s;
                '''
        response_query = connectToMySQL('wall_db').query_db(query,data) 
        return response_query

    @classmethod
    def get_all_received_messages(cls,data):
        query = '''
                SELECT messages.id,messages.message,messages.created_at,messages.updated_at, senders.id,senders.first_name,senders.last_name,senders.created_at,senders.updated_at FROM users 
                LEFT JOIN messages ON users.id = messages.recipient_id
                LEFT JOIN users AS senders ON  messages.user_id= senders.id
                WHERE users.id= %(id)s ;
                '''
        response_query_messages=connectToMySQL('wall_db').query_db(query,data)
        messages=[]
        for message_senders in response_query_messages:
            sender = {
            'id':message_senders['senders.id'],
            'first_name':message_senders['first_name'],
            'last_name':message_senders['last_name'],
            'email':None,
            'password':None,
            'created_at':None,
            'updated_at':None
            }
            sender = user_model.User(sender)
            data = {
            'id':message_senders['id'],
            'message':message_senders['message'],
            'user_id':sender,
            'recipient_id':None,
            'created_at':message_senders['created_at'],
            'updated_at':message_senders['updated_at']
            }
            messages.append(cls(data))
        return messages
    
    @staticmethod
    def validate_delete_message(data,id):
        is_valid=True
        all_messages=Message.get_all_received_messages(data)
        count=0
        for message in all_messages:
            if message.id==id:
                count += 1
        if count != 1:
              is_valid = False
        return is_valid