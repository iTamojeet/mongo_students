from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://admin:989144@clusterx.mke2gdh.mongodb.net/?retryWrites=true&w=majority&appName=ClusterX")
db = client["school"]  # Use database named "school"
students = db["students"]  # Collection named "students"

# Home route (renders HTML page)
@app.route('/')
def home():
    return render_template("home.html")

# ----------------------------- #
#         CREATE STUDENT        #
# ----------------------------- #
@app.route("/create", methods=["POST"])
def create_student():
    # Check if data is sent as JSON
    if request.is_json:
        body = request.get_json()

        # Prepare data dictionary with nested "subjects"
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
        students.insert_one(data)  # Insert into MongoDB
        return "Student inserted successfully via JSON!"

    else:
        # If data is submitted via HTML form
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

# ----------------------------- #
#         READ STUDENTS         #
# ----------------------------- #
@app.route('/view', methods=['GET'])
def read_students():
    result = []
    for s in students.find():
        s['_id'] = str(s['_id'])  # Convert ObjectId to string for JSON
        result.append(s)
    return jsonify(result)  # Return all student records as JSON

# ----------------------------- #
#         UPDATE STUDENT        #
# ----------------------------- #
@app.route('/update/<id>', methods=['PUT'])
def update_student(id):
    data = request.json  # Get update fields from request body
    students.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    return jsonify({"msg": "Student updated."})

# ----------------------------- #
#         DELETE STUDENT        #
# ----------------------------- #
@app.route('/delete/<id>', methods=['DELETE'])
def delete_student(id):
    students.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Student deleted."})

# ----------------------------- #
#         RUN THE SERVER        #
# ----------------------------- #
if __name__ == "__main__":
    app.run(debug=True)
