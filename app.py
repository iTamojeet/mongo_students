from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb+srv://admin:989144@clusterx.mke2gdh.mongodb.net/?retryWrites=true&w=majority&appName=ClusterX")
db = client["school"]
students = db["students"]

@app.route('/')
def home():
    return render_template("home.html")

# Create
@app.route("/create", methods=["POST"])
def create_student():
    if request.is_json:
        body = request.get_json()

        # Use nested "subjects" directly
        data = {
            "name": body.get("name"),
            "address": body.get("address"),
            "email": body.get("email"),
            "subjects": {
                "name": body.get("subjects", {}).get("name"),
                "author": body.get("subjects", {}).get("author"),
                "description": body.get("subjects", {}).get("description")
            }
        }

        print("Data to insert:", data)
        students.insert_one(data)
        return "Student inserted successfully via JSON!"
    
    else:
        # Handle HTML form
        form = request.form
        data = {
            "name": form.get("name"),
            "address": form.get("address"),
            "email": form.get("email"),
            "subjects": {
                "name": form.get("subject_name"),
                "author": form.get("subject_author"),
                "description": form.get("subject_description")
            }
        }

        students.insert_one(data)
        return "Student inserted successfully via form!"


# Read All
@app.route('/view', methods=['GET'])
def read_students():
    result = []
    for s in students.find():
        s['_id'] = str(s['_id'])
        result.append(s)
    return jsonify(result)

# Update
@app.route('/update/<id>', methods=['PUT'])
def update_student(id):
    data = request.json
    students.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"msg": "Student updated."})

# Delete
@app.route('/delete/<id>', methods=['DELETE'])
def delete_student(id):
    students.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Student deleted."})

if __name__ == "__main__":
    app.run(debug=True)
