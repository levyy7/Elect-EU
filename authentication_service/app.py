from flask import Flask
from controllers.auth_controller import auth_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)