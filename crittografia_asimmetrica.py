from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding 
from cryptography.hazmat.backends import default_backend

def generate_key_pair():
    # Genera una coppia di chiavi RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(message, public_key):
    # Cifra il messaggio utilizzando la chiave pubblica
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def decrypt_message(encrypted_message, private_key):
    # Decifra il messaggio utilizzando la chiave privata
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()

# Genera una coppia di chiavi
private_key, public_key = generate_key_pair()

# Messaggio da crittografare
message = "Questo è un messaggio segreto!"

# Crittografa il messaggio
encrypted_message = encrypt_message(message, public_key)

# Stampa il messaggio crittografato
print("Messaggio crittografato:", encrypted_message)

# Decrittografa il messaggio
decrypted_message = decrypt_message(encrypted_message, private_key)

# Stampa il messaggio decrittografato
print("Messaggio decrittografato:", decrypted_message)