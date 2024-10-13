from flask import Flask, jsonify, abort, request
import mariadb
import urllib.parse

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False  # pour utiliser l'UTF-8 plutot que l'unicode


def execute_query(query, data=()):
    config = {
        'host': 'mariadb',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'bd_bibliotheque'
    }
    """Execute une requete SQL avec les param associés"""
    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute(query, data)

    if cur.description:
        # serialize results into JSON
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        list_result = []
        for result in rv:
            list_result.append(dict(zip(row_headers, result)))
        return list_result
    else:
        conn.commit()
        return cur.lastrowid


# we define the route /
@app.route('/')
def welcome():
    liens = [{}]
    liens[0]["_links"] = [{
        "href": "/auteurs",
        "rel": "auteurs"
    }, {
        "href": "/livres",
        "rel": "livres"
    },
    {
        "href": "/categories",
        "rel": "categories"
    },
    ]
    return jsonify(liens), 200


""" ################## AUTEURS ##################
    #############################################"""

# Récupérer la liste de tous les auteurs
@app.route('/auteurs', methods=['GET'])
def get_auteurs():
    """Récupère la liste des auteurs"""
    auteurs = execute_query("SELECT * FROM auteurs")
    for i in range(len(auteurs)):
        auteurs[i]["_links"] = [{
            "href": f"/auteurs/{auteurs[i]['nom']}",
            "rel": "self"
        }]
    return jsonify(auteurs), 200

# Récupérer un auteur spécifique par son nom
@app.route('/auteurs/<string:nom>', methods=['GET'])
def get_auteur(nom):
    """Récupère les détails d'un auteur spécifique par son nom"""
    auteur = execute_query("SELECT * FROM auteurs WHERE nom = ?", (nom,))
    if not auteur:
        abort(404, description="Auteur non trouvé")
    # Ajout des liens _links pour l'auteur trouvé
    auteur[0]["_links"] = [{
        "href": f"/auteurs/{auteur[0]['nom']}/livres",
        "rel": "livres"
    }]
    return jsonify(auteur[0]), 200

# Ajouter un nouvel auteur
@app.route('/auteurs', methods=['POST'])
def post_auteur():
    """Ajoute un auteur"""
    nom = request.args.get("nom")
    if not nom:
        abort(400, description="Le champ 'nom' est requis.")
    execute_query("INSERT INTO auteurs (nom) VALUES (?)", (nom,))
    # On renvoie le lien de l'auteur que l'on vient de créer
    reponse_json = jsonify({
        "_links": [{
            "href": f"/auteurs/{urllib.parse.quote(nom)}",
            "rel": "self"
        }]
    })
    return reponse_json, 201  # Created

# Supprimer un auteur par son nom
@app.route('/auteurs/<string:nom>', methods=['DELETE'])
def delete_auteur(nom):
    """Supprimer un auteur par son nom"""
    execute_query("DELETE FROM auteurs WHERE nom = ?", (nom,))
    return "", 204  # No Content

""" ################## CATEGORIES ##################
    #############################################"""

# Récupérer la liste de toutes les catégories
@app.route('/categories', methods=['GET'])
def get_categories():
    """Récupère la liste des catégories"""
    categories = execute_query("SELECT * FROM categories")
    for i in range(len(categories)):
        categories[i]["_links"] = [{
            "href": f"/categories/{categories[i]['nom']}",
            "rel": "self"
        }]
    return jsonify(categories), 200

# Récupérer une catégorie spécifique par son nom
@app.route('/categories/<string:nom>', methods=['GET'])
def get_categorie(nom):
    """Récupère les détails d'une catégorie spécifique par son nom"""
    categorie = execute_query("SELECT * FROM categories WHERE nom = ?", (nom,))
    if not categorie:
        abort(404, description="Catégorie non trouvée")
    # Ajout des liens _links pour la catégorie trouvée
    categorie[0]["_links"] = [{
        "href": f"/categories/{categorie[0]['nom']}/livres",
        "rel": "livres"
    }]
    return jsonify(categorie[0]), 200

# Ajouter une nouvelle catégorie
@app.route('/categories', methods=['POST'])
def post_categorie():
    """Ajoute une nouvelle catégorie"""
    nom = request.args.get("nom")
    if not nom:
        abort(400, description="Le champ 'nom' est requis.")
    execute_query("INSERT INTO categories (nom) VALUES (?)", (nom,))
    reponse_json = jsonify({
        "_links": [{
            "href": f"/categories/{urllib.parse.quote(nom)}",
            "rel": "self"
        }]
    })
    return reponse_json, 201  # Created

# Supprimer une catégorie par son nom
@app.route('/categories/<string:nom>', methods=['DELETE'])
def delete_categorie(nom):
    """Supprimer une catégorie par son nom"""
    execute_query("DELETE FROM categories WHERE nom = ?", (nom,))
    return "", 204 


""" ################## LIVRES ##################
    #############################################"""

@app.route('/livres', methods=['GET'])
def get_livres():
    """Récupère la liste de tous les livres"""
    livres = execute_query("SELECT * FROM livres")
    for livre in livres:
        livre["_links"] = [
            {
                "href": f"/livres/{livre['isbn']}",
                "rel": "self"
            },
            {
                "href": f"/livres/{livre['isbn']}/auteurs",
                "rel": "auteurs"
            }
        ]
    return jsonify(livres), 200


@app.route('/livres/<string:isbn>', methods=['GET'])
def get_livre_by_isbn(isbn):
    """Récupère les détails d'un livre spécifique par son ISBN"""
    livre = execute_query("SELECT * FROM livres WHERE isbn = ?", (isbn,))
    if not livre:
        abort(404, description="Livre non trouvé")
    
    livre[0]["_links"] = [
        {
            "href": f"/livres/{isbn}",
            "rel": "self"
        },
        {
            "href": f"/livres/{isbn}/auteurs",
            "rel": "auteurs"
        }
    ]
    return jsonify(livre[0]), 200

@app.route('/livres/<string:isbn>/auteurs', methods=['GET'])
def get_auteurs_by_livre(isbn):
    """Récupère les auteurs associés à un livre spécifique"""
    auteurs = execute_query("""
        SELECT auteurs.nom FROM auteurs
        JOIN livres ON livres.auteur_id = auteurs.id
        WHERE livres.isbn = ?
    """, (isbn,))
    
    if not auteurs:
        abort(404, description="Aucun auteur trouvé pour ce livre")
    
    for i in range(len(auteurs)):
        auteurs[i]["_links"] = [{
            "href": "/auteurs/" + auteurs[i]["nom"],
            "rel": "self"
        }]
    return jsonify(auteurs), 200


@app.route('/auteurs/<string:nom_auteur>/categories/<string:nom_categorie>/livres', methods=['POST'])
def post_livre(nom_auteur, nom_categorie):
    """Ajoute un livre à un auteur et une catégorie spécifiques"""
    isbn = request.args.get('isbn')
    nom_livre = request.args.get('nom')
    description = request.args.get('description')
    if not isbn or not nom_livre or not description:
        abort(400, description="Les champs 'isbn', 'nom', 'description' sont requis.")
    execute_query("""
        INSERT INTO livres (isbn, nom, description, auteur_id, categorie_id)
        VALUES (?, ?, ?, 
                (SELECT id FROM auteurs WHERE nom = ?),
                (SELECT id FROM categories WHERE nom = ?))
    """, (isbn, nom_livre, description, nom_auteur, nom_categorie))
    reponse_json = jsonify({
        "_links": [{
            "href": f"/livres/{isbn}",
            "rel": "self"
        }]
    })
    return reponse_json, 201  # Created


@app.route('/livres/<string:isbn>', methods=['DELETE'])
def delete_livre(isbn):
    """Supprime un livre par son ISBN"""
    result = execute_query("DELETE FROM livres WHERE isbn = ?", (isbn,))
    if result == 0:
        abort(404, description="Livre non trouvé")
    
    return "", 204 


@app.route('/categories/<string:nom_categorie>/livres', methods=['GET'])
def get_livres_by_categorie(nom_categorie):
    """Récupère la liste des livres dans une catégorie spécifique"""
    livres = execute_query("""
        SELECT * FROM livres
        JOIN categories ON livres.categorie_id = categories.id
        WHERE categories.nom = ?
    """, (nom_categorie,))
    
    if not livres:
        abort(404, description="Aucun livre trouvé dans cette catégorie")  
    for livre in livres:
        livre["_links"] = [
            {
                "href": f"/livres/{livre['isbn']}",
                "rel": "self"
            },
            {
                "href": f"/livres/{livre['isbn']}/auteurs",
                "rel": "auteurs"
            }
        ]
    return jsonify(livres), 200

if __name__ == '__main__':
    # define the localhost ip and the port that is going to be used
    app.run(host='0.0.0.0', port=5000)
