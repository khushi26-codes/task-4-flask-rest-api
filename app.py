from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store (Dictionary)
users = {}
user_id_counter = 1

# HOME Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to User Management API"})

# GET - Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET - Get single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# POST - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    new_user = {
        "id": user_id_counter,
        "name": data['name'],
        "email": data['email']
    }
    users[user_id_counter] = new_user
    user_id_counter += 1
    return jsonify(new_user), 201

# PUT - Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    users[user_id]['name'] = data.get('name', users[user_id]['name'])
    users[user_id]['email'] = data.get('email', users[user_id]['email'])
    return jsonify(users[user_id]), 200

# DELETE - Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    del users[user_id]
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
