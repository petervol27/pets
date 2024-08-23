from flask import Flask, jsonify, request


app = Flask(__name__)

pet1 = {
    "id": 1,
    "name": "Dixie",
    "age": 4,
    "img": "https://www.jesuitroundup.org/wp-content/uploads/2018/01/tabby-cat-names.jpg",
}
pet2 = {
    "id": 2,
    "name": "Charlie",
    "age": 0.5,
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrmojuD-xMi5uPUpCwC6b-Z0dFubMSpZXRAA&s",
}
pets = [pet1, pet2]


@app.route("/pets/")
def pets_list():
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


@app.route("/add_pet/", methods=["POST"])
def add_pet():
    pet = request.json
    pets.append(pet)
    return jsonify({"response": "success"})


if __name__ == "__main__":
    app.run(debug=True)
