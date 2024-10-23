from dotenv import load_dotenv
from flask import Flask
from controllers import users

app = Flask(__name__)

app.add_url_rule('/api/users', view_func=users.get_all_users, methods=["GET"])
app.add_url_rule('/api/users', view_func=users.create_user, methods=["POST"])
app.add_url_rule('/api/users/<user_id>', view_func=users.get_user_by_id, methods=["GET"])
app.add_url_rule('/api/users/<user_id>', view_func=users.update_user_by_id, methods=["PUT"])
app.add_url_rule('/api/users/<user_id>', view_func=users.delete_user_by_id, methods=["DELETE"])

if __name__ == '__main__':
    load_dotenv()
    app.run()
