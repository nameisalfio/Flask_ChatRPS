# Flask_ChatRPS

Flask_ChatRPS is a web application that integrates a Rock-Paper-Scissors (RPS) classifier with user authentication features. This project is designed to demonstrate the use of machine learning models in a Flask-based web application, focusing on classifying images of hand gestures for the RPS game and managing user accounts.

## Features

- **User Authentication**: Users can register, log in, and manage their profiles. Passwords are hashed using Werkzeug's secure password hashing utilities to ensure user credentials are protected.
- **RPS Classifier Integration**: The application includes an RPS classifier model that recognizes hand gestures for Rock, Paper, Scissors. The model is loaded and utilized in the Flask application to predict the user's gesture from uploaded images.
- **Responsive UI**: The web interface is designed with HTML, CSS, and JavaScript to provide a user-friendly experience.

## Installation

1. **Clone the repository**:

   ```bash
   git clone git@github.com:nameisalfio/Flask_ChatRPS.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Flask_ChatRPS
   ```

3. **Create and activate a Conda environment**:

    ```bash
    conda env create -f environment.yml
    conda activate chat_rps
    ```

4. **Install dependencies**:

  ```bash
  pip install -r requirements.txt
  ```

5. **Run database migrations**:

  ```bash
  flask db upgrade
  ```

6. **Run the application**:

  ```bash
  python -m ChatRPS.run
  ```

  or if you have the `FLASK_APP` environment variable set:

  ```bash
  flask run
  ```

  Script for setting the `FLASK_APP` environment variable:

  ```bash
  export FLASK_APP=ChatRPS
  export FLASK_ENV=development
  export FLASK_DEBUG=1
  ```

## How It Works

### RPS Classifier

The RPS classifier is built using a convolutional neural network (CNN) with multiple layers of convolution, batch normalization, activation, pooling, and dropout. The model processes input images of hand gestures and classifies them into one of three categories: Rock, Paper, or Scissors. The model's architecture is designed to effectively capture features from the images and make accurate predictions.

### User Authentication

The user authentication system uses Flask sessions to manage user login states. Passwords are stored in the database as hashed values, enhancing security by protecting user credentials from unauthorized access. Users can register, log in, update their profiles, and log out through the provided routes.

## Project Structure

The project structure is as follows:

```bash
Flask_ChatRPS
├── ChatRPS
│   ├── __init__.py
│   ├── app
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── ml_models
│   │   │   ├── rps_classifier.py
│   │   │   └── rps_model.pth
│   │   ├── models
│   │   │   └── user.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   ├── rps_routes.py
│   │   │   └── user_routes.py
│   │   ├── static
│   │   │   ├── css
│   │   │   │   └── style.css
│   │   │   ├── img
│   │   │   │   ├── paper.png
│   │   │   │   ├── paper2.png
│   │   │   │   ├── rock.png
│   │   │   │   ├── rock2.png
│   │   │   │   ├── scissors.png
│   │   │   │   └── scissors2.png
│   │   │   └── js
│   │   └── templates
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── profile.html
│   │       ├── register.html
│   │       ├── rps_classify.html
│   │       └── update_form.html
│   ├── migrations
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── script.py.mako
│   └── run.py
├── LICENSE
├── README.md
├── environment.yml
└── requirements.txt
```

It consists of the following components:

It consists of the following components:

- **`ChatRPS/`**: Contains the main application package.
  - **`app/`**: Holds the core application logic and components.
    - **`__init__.py`**: Initializes the Flask application and sets up configurations.
    - **`config.py`**: Contains configuration settings for the application.
    - **`ml_models/`**: Contains the RPS classifier model and related code.
      - **`rps_classifier.py`**: Defines the RPS classifier logic.
      - **`rps_model.pth`**: Pre-trained model weights.
    - **`models/`**: Defines data models, such as the user model for authentication.
      - **`user.py`**: Contains the User model and related database operations.
    - **`routes/`**: Defines application routes.
      - **`__init__.py`**: Registers the blueprints for the application routes.
      - **`auth_routes.py`**: Handles authentication-related routes.
      - **`rps_routes.py`**: Handles routes related to the RPS game functionality.
      - **`user_routes.py`**: Manages user profile and settings routes.
    - **`static/`**: Contains static files such as CSS, images, and JavaScript.
      - **`css/`**: Contains stylesheets.
        - **`style.css`**: Main stylesheet for the application.
      - **`img/`**: Contains images used in the application.
        - **`paper.png`, `rock.png`, `scissors.png`, etc.**: Images for RPS gestures.
      - **`js/`**: Contains JavaScript files.
    - **`templates/`**: Contains HTML templates for rendering web pages.
      - **`base.html`**: Base template used for other templates.
      - **`login.html`, `profile.html`, `register.html`, etc.**: Templates for various pages.
  - **`migrations/`**: Holds database migration scripts.
    - **`README`**: Documentation for migrations.
    - **`alembic.ini`**: Configuration for Alembic migrations.
    - **`env.py`**: Environment settings for migrations.
    - **`script.py.mako`**: Template for migration scripts.
  - **`run.py`**: Entry point for running the Flask application.
- **`LICENSE`**: Contains the project's license information.
- **`README.md`**: This file, providing an overview and documentation for the project.
- **`environment.yml`**: Contains Conda environment configuration and dependencies.
- **`requirements.txt`**: Contains pip dependencies.

## Best Practices

- **Modular Design**: The application is divided into multiple modules to separate concerns, making it easier to manage and extend. For instance, routes, models, and machine learning components are organized into their respective directories.
- **Blueprints**: Flask blueprints are used to organize routes into logical components. Each blueprint handles a specific aspect of the application, such as authentication or RPS functionality, which enhances code maintainability.
- **Configuration Management**: Configuration settings are kept in `config.py` to separate them from application logic and facilitate different configurations for development, testing, and production environments.
- **Security**: Passwords are hashed before storing them in the database, and user sessions are managed securely using Flask sessions.
- **Database Management**: SQLAlchemy is used for ORM (Object-Relational Mapping) to handle database operations, providing a high-level abstraction for database interactions.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The RPS classifier model was developed as part of a machine learning project to classify hand gestures.
- Flask and related libraries are used for building the web application and handling user authentication.
