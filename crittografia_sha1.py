import hashlib

def sha1_hash(message):
    # Crea un oggetto hash SHA-1
    sha1 = hashlib.sha1()
    # Aggiunge il messaggio al calcolo dell'hash
    sha1.update(message.encode())
    # Calcola l'hash SHA-1
    hashed_message = sha1.hexdigest()
    return hashed_message

# Messaggio da crittografare
message = "Questo è un messaggio da crittografare con SHA-1"

# Calcola l'hash SHA-1 del messaggio
hashed_message = sha1_hash(message)

# Stampa l'hash SHA-1
print("Hash SHA-1:", hashed_message)