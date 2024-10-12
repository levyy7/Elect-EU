from controllers.auth_controller import auth_blueprint
from app import app

app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
