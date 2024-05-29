import os
import certifi

# Ensure SSL_CERT_FILE is set
os.environ["SSL_CERT_FILE"] = certifi.where()
