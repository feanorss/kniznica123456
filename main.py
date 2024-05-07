from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ucrksoznquj3b71nfqcv:2YKt1zZxmkqsYgV41W3260QJNXRTn6@bphzurc4badokyq3ezig-postgresql.services.clever-cloud.com:50013/bphzurc4badokyq3ezig"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from Authors import Author
from Members import Member

@app.route("/authors",methods=["GET"])
def getAuthors():
    authors = Author.query.all()
    author_list = [auth.to_dict() for auth in authors]
    return jsonify(author_list)

@app.route("/members",methods=["GET"])
def getMembers():
    members = Member.query.all()
    member_list = [mem.to_dict() for mem in members]
    return jsonify(member_list)

@app.route("/members/<int:member_id>", methods=["GET"])
def getMember(member_id):
    member = Member.query.get(member_id)
    if member:
        member_dict = member.to_dict()
        return jsonify(member_dict)
    else:
        return jsonify({"error": "Member not found"}), 404

@app.route("/members/reg", methods=["POST"])
def register_member():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    pasword = data.get('password')

    if not (first_name and last_name and email and pasword):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new Member object
    new_member = Member(first_name=first_name, last_name=last_name, email=email, pasword=pasword)

    # Add the new member to the database session
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Member registered successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)

