# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Flask-WTForm](https://flask-wtf.readthedocs.io/en/stable/#) is an extension to check form request data and have an easy way to create forms

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

## API Documentation

- ### GET /drinks
    Get drinks with short format
  
    Example JSON response:
    ```
      {
      "drinks": [
        {
          "id": 4, 
          "recipe": [
            {
              "color": "green", 
              "parts": 1
            },
            {
              "color": "darkgreen", 
              "parts": 2
            }
          ], 
          "title": "Mocha Drink"
        }
      ], 
      "success": true
    }
    ```
  
- ### GET /drinks-detail
    Get drinks with long format. You need _**get:drinks-detail**_ permission for this
  
    Example JSON response:
    ```
      {
      "drinks": [
        {
          "id": 4, 
          "recipe": [
            {
              "name": "Tea",
              "color": "green", 
              "parts": 1
            },
            {
              "name": "Mocha",
              "color": "darkgreen", 
              "parts": 2
            }
          ], 
          "title": "Mocha Drink"
        },
        ...
      ], 
      "success": true
    }
    ```

- ### POST /drinks
    Endpoint to create a new drink. You need _**post:drinks**_ permission for this
    
    JSON parameters:
    - **title**: Name of the new drink
    - **recipe**: Array containing all parts of the drink
    - **recipe.\*.name**: Name of the drink part
    - **recipe.\*.color**: Color of part to show. All CSS colors formats are ok
    - **recipe.\*.parts**: Number of parts of recipe element
    
    Example JSON request:
    ```
    {
        "title":"Mocha Drink",
        "recipe":[
            {
                "name": "Tea",
                "color": "green",
                "parts": 1
            }, {
                "name": "Mocha",
                "color": "darkgreen",
                "parts": 2
            }
        ]
    }
    ```
  
    Example JSON response:
    ```
      {
        "drinks": [
        {
          "id": 4, 
          "recipe": [
            {
              "color": "green", 
              "parts": 1
            },
            {
              "color": "darkgreen", 
              "parts": 2
            }
          ], 
          "title": "Mocha Drink"
        }
      ], 
      "success": true
    }
    ```
  
- ### PATCH /drinks/<int:drink_id>
    Endpoint to create a new drink. You need _**patch:drinks**_ permission for this
    
    URL parameters:
    - **drink_id**: Id of drink to edit
    
    JSON parameters:
    - **title**: Name of the new drink
    - **recipe**: Array containing all parts of the drink
    - **recipe.\*.name**: Name of the drink part
    - **recipe.\*.color**: Color of part to show. All CSS colors formats are ok
    - **recipe.\*.parts**: Number of parts of recipe element
    
    Example JSON request:
    ```
    {
        "title":"Super Mocha Drink",
        "recipe":[
            {
                "name": "Super-Tea",
                "color": "#00ff00",
                "parts": 1
            }, {
                "name": "Super-Mocha",
                "color": "darkgreen",
                "parts": 2
            }
        ]
    }
    ```
  
    Example JSON response:
    ```
      {
        "drinks": [
        {
          "id": 4, 
          "recipe": [
            {
                "name": "Super-Tea",
                "color": "#00ff00",
                "parts": 1
            },
            {
                "name": "Super-Mocha",
                "color": "darkgreen",
                "parts": 2
            }
          ], 
          "title": "Super Mocha Drink"
        }
      ], 
      "success": true
    }
    ```
  
- ### DELETE /drinks/<int:drink_id>
    Delete the specified drink. You need _**delete:drinks**_ permission for this
    
    URL parameters:
    - **drink_id**: Id of drink to delete
  
    Example JSON response:
    ```
    {
        "drink": 4, <-- id of deleted drink
        "success": true
    }
    ```