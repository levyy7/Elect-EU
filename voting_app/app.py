from app import app
import os

cert_file = "/certs/localhost+2.pem"
key_file = "/certs/localhost+2-key.pem"


def run_app():
    # Check if the certificate and key files exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        # If both exist, run with SSL context (HTTPS)
        print("Running with SSL context")
        app.run(ssl_context=(cert_file, key_file), host="0.0.0.0", port=5000)
    else:
        # If the files don't exist, run without SSL (HTTP)
        print("Running without SSL context")
        app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    run_app()
