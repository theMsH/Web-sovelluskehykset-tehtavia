from dotenv import load_dotenv
from flask import Flask
from controllers import users

app = Flask(__name__)

app.add_url_rule('/api/users', view_func=users.get_all_users, methods=["GET"])
app.add_url_rule('/api/users/<user_id>', "user_id", users.get_user_by_id, methods=["GET"])

if __name__ == '__main__':
    load_dotenv()
    app.run()
