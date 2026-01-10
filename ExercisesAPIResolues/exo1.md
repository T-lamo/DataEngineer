# Partie 1 – Analyse critique d’une API

On vous fournit les endpoints **User** d’une API REST existante :

```http
POST /getUser
GET /deleteUser?id=12
POST /updateUser
```

1. Utilisation des méthodes HTTP


## Utilisation des méthodes HTTP
Les méthodes HTTP sont mal employées :

### POST /getUser

La méthode POST est utilisée pour récupérer une ressource, ce qui est incorrect.

En REST, la récupération de données doit se faire avec GET.

### GET /deleteUser?id=12

La méthode GET ne doit jamais modifier l’état du serveur.

Ici, elle est utilisée pour supprimer une ressource, ce qui viole le principe de sécurité et d’idempotence de GET.

La méthode appropriée serait DELETE.

### POST /updateUser

POST est réservé à la création de nouvelles ressources.
## Structure des URLs
2- Le nom de l'endpoint ne respecte pas le standard: la bonne manière de faire: GET /user 
## Sémantique REST

3- en Rest les urls doivent representer des ressources et non des actions. /getUser => /users, 


### Caractère complet ou incomplet des endpoints

Les endpoints proposés sont incomplets :

Aucun endpoint clair pour :

- créer un utilisateur (POST /users)

- récupérer la liste des utilisateurs (GET /users)

- récupérer un utilisateur par ID de façon standard (GET /users/1)

L’identifiant (id) est parfois passé en query (?id=12) au lieu d’être dans l’URL


# Partie 2 – Refonte et conception d’une API REST

## Création un utilisateur
  - Méthode : POST
  - Endpoint : /users
  - Payload: 
        ``` {
        "email": "user@test.com",
        "full_name": "John Doe",
        "age": 32,
        "is_active": true
        } ```
        
  - Code de réponse:  
        - 201 (Created)
        - 400 Bad request (Mauvais format)
        - 401 unauthorized (Pas connecté)
        - 403 forbidden (pas de droit)
        - 409 (déjà créé)

## récupérer tous les utilisateurs
- Méthode : GET
- Endpoint : /users
- Code de réponse: 
        - 200 ok
        - 204 No content
        - 401 unauthorized (Pas connecté)
        - 403 forbidden (pas de droit)
## récupérer un utilisateur unique
- Méthode : GET
- Endpoint : /users/{id}
- Code de réponse : 
        - 200 ok
        - 400 bad request
        - 401 unauthorized (Pas connecté)
        - 403 forbidden (pas de droit)
        - 404 not found


## mettre à jour un utilisateur
- Méthode : PUT (ou PATCH)
- Endpoint : /users/{id}
- Payload : 
  ``` 
    {
  "full_name": "John Doe Updated",
  "age": 33,
  "is_active": false
}```
- Code de réponse: 
        - 201 ok (PUT)
        - 200 ok
        - 400 bad request
        - 401 unauthorized (Pas connecté)
        - 403 forbidden (pas de droit)
        - 404 not found
        - 409 (déjà créé)




## supprimer un utilisateur
- Méthode : DELETE
- Endpoint : /users/{id}
- Code de réponse : 
        - 200 ok
        - 204 no content
        - 400 bad request
        - 401 unauthorized (Pas connecté)
        - 403 forbidden (pas de droit)
        - 404 not found




## Partie 1 - Annalyse des données

```
{
"email": "user@test.com",
"full_name": "John Doe",
"age": 32,
"is_active": true
} 
```

### 2 Les champs qui doivent etre stockés en base de données
  - id
  - email
  - prenom
  - nom
  - is_active
  - age


### 2 Les champs qui doivent etre stockés en base de données
  - Type de données SQLModel
    - email : str
    - prenom : str
    - nom : str
    - is_active: bool
    - age: int


  - Clé primaire (id)
  - unique (email)
  - nullable (age)
  - valeur par défaut (is_active)
  - obligatoire (email, nom, prenom)



## Partie 2 - Annalyse des données
### l’API accède directement aux tables de la base de données
    - Exposition involontaire de données sensibles
    - Contrôles d’accès insuffisants
    - Escalade de privilèges
### Exécute des requêtes SQL construites à partir des données reçues des clients
   - Injection SQL (SQL Injection)
   - Accès au modification non autorisées





