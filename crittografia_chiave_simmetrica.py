from cryptography.fernet import Fernet

def generate_key():
    # Genera una chiave casuale
    key = Fernet.generate_key()
    return key

def encrypt_message(message, key):
    # Crea un oggetto Fernet utilizzando la chiave
    fernet = Fernet(key)
    # Cripta il messaggio
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    # Crea un oggetto Fernet utilizzando la chiave
    fernet = Fernet(key)
    # Decifra il messaggio
    decrypted_message = fernet.decrypt(encrypted_message)
    return decrypted_message.decode()

# Genera una chiave
key = generate_key()

# Messaggio da crittografare
message = "Questo è un messaggio segreto!"

# Crittografa il messaggio
encrypted_message = encrypt_message(message, key)

# Stampa il messaggio crittografato
print("Messaggio crittografato:", encrypted_message)

# Decrittografa il messaggio
decrypted_message = decrypt_message(encrypted_message, key)

# Stampa il messaggio decrittografato
print("Messaggio decrittografato:", decrypted_message)