from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
load_dotenv()
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "https://pets-1-zk5k.onrender.com",
                "https://petervol27.github.io",
                "https://pets-front.onrender.com",
                "http://127.0.0.1:5500",
            ]
        }
    },
)


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("db_host"),
        database=os.getenv("db_name"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        port=os.getenv("db_port"),
    )
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS pets(id SERIAL PRIMARY KEY,name VARCHAR(50),age INT,img TEXT,animal VARCHAR(20))"
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
            "INSERT INTO pets(name,img,age,animal) VALUES(%s,%s,%s,%s)",
            (
                new_pet.get("name"),
                new_pet.get("img"),
                new_pet.get("age"),
                new_pet.get("animal"),
            ),
        )
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({"response": "Added succesfully"})
        else:
            return jsonify({"response": "Failed to add pet"})
    cursor.execute("SELECT * FROM pets")
    rows = cursor.fetchall()
    pets = [dict(row) for row in rows]
    conn.close()
    return jsonify(pets)


@app.route("/pets/<int:id>/")
def get_pet(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SELECT * FROM pets WHERE id=%s", (id,))
    row = cursor.fetchone()
    if row:
        conn.close()
        return jsonify(dict(row))
    else:
        return jsonify({"response": "Pet not found"})


@app.route("/pets/<int:id>/", methods=["DELETE"])
def delete_pet(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("DELETE FROM pets WHERE id=%s", (id,))
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        return jsonify({"response": "Deleted succesfully"})
    else:
        return jsonify({"response": "Pet not found"})


@app.route("/pets/<int:id>", methods=["PUT"])
def edit_pet(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    data = request.json
    columns = ", ".join([f"{key} =%s" for key in data.keys()])
    values = list(data.values())
    values.append(id)
    query = f"UPDATE pets SET {columns} WHERE id = %s"
    cursor.execute(query, tuple(values))
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        return jsonify({"response": "Edited succesfully"})
    else:
        return jsonify({"response": "Pet not found"})


@app.route("/pets/search/")
def search():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    search_value = request.args.get("searchValue")
    if search_value.lower == "dog" or search_value == "cat":
        cursor.execute("SELECT * FROM pets WHERE animal =%s", (search_value,))
    else:
        cursor.execute("SELECT * FROM pets WHERE name ILIKE %s ", (search_value + "%",))
    rows = cursor.fetchall()
    try:
        pets = [dict(row) for row in rows]
        return pets
    except Exception as ex:
        print(ex)
        return jsonify({"response": "Pet not found"})


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
