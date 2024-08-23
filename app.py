from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)


def get_connection():
    conn = psycopg2.connect(
        "postgresql://pets_db_m8f9_user:FGG6CIxeAw1HkNlGzJOk6vtV0OIazkXe@dpg-cr456c08fa8c73dgnk5g-a.frankfurt-postgres.render.com/pets_db_m8f9"
    )
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS pets(id SERIAL PRIMARY KEY,name VARCHAR(50),age INT,img TEXT)"
    )
    conn.commit()
    conn.close()


@app.route("/pets/", methods=["GET", "POST"])
def pets_list():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    if request.method == "POST":
        new_pet = request.json
        cursor.execute(
            "INSERT INTO pets(name,img,age) VALUES(%s,%s,%s)",
            (new_pet.get("name"), new_pet.get("img"), new_pet.get("age")),
        )
        conn.commit()
        conn.close()
        return jsonify({"response": "Added succesfully"})
    cursor.execute("SELECT * FROM pets")
    rows = cursor.fetchall()
    pets = [dict(row) for row in rows]
    conn.close()
    return jsonify(pets)


@app.route("/pets/<id>/")
def get_pet(id):
    try:
        pet = [pet for pet in pets if pet.get("id") == int(id)]
        if pet:
            return jsonify(pet)
        else:
            return jsonify({"respones": "No pet found"})
    except Exception as e:
        return jsonify({"response": "suka blyat not cat! Not ID not worky!"})


@app.route("/pets/<int:id>", methods=["DELETE"])
def delete_pet(id):
    pet_to_delete = [pet for pet in pets if pet.get("id") == id]
    if pet_to_delete:
        print(pet_to_delete[0])
        pets.remove(pet_to_delete[0])
        return jsonify({"response": "Deleted succesfully"})
    else:
        return jsonify({"response": "No Pet Found!! "})


@app.route("/pets/<int:id>", methods=["PUT"])
def edit_pet(id):
    changes = request.json
    for pet in pets:
        if pet.get("id") == id:
            pet.update(changes)
            return jsonify({"response": "Edited succesfully"})
        else:
            return jsonify({"response": "No Pet Found!! "})


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
