from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://birehan:password@localhost/user_db'
db = SQLAlchemy(app)
CORS(app)

# Define the User model
class User(db.Model):
    def __init__(self, user_name,email,password ):
        self.user_name = user_name
        self.email=email
        self.password = password


    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


  
# ... Other models and helper functions ...

# Create tables
with app.app_context():
    db.create_all()

def format_user(event):
    return {
        "user_name": event.user_name,
        "email": event.email,
        "id": event.id,
        "password":event.password
    }


# Route to get a user by ID
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Find the user in the database by ID
    user = User.query.get(user_id)

    if user:
        # If the user is found, format and return the user data
        return jsonify({"user": format_user(user)})
    else:
        # If the user is not found, return a 404 response
        return jsonify({"message": "User not found"}), 404



# Routes for User CRUD operations
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(user_name=data['user_name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": format_user(new_user)})


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user.user_name = data.get('user_name', user.user_name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": format_user(user)})

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [format_user(user) for user in users]
    return jsonify({"users": user_list})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# ... Other routes and code ...

if __name__ == '__main__':
    app.run()

