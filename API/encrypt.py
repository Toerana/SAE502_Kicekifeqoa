import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

def encrypt_file(input_file, output_file, key):
    # Deriver une clé de 32 octets à partir de la clé de 64 octets
    derived_key = hashlib.sha256(key).digest()

    # Créer un vecteur d'initialisation
    iv = os.urandom(AES.block_size)  # Générer un IV aléatoire

    # Créer le cipher AES
    cipher = AES.new(derived_key, AES.MODE_CBC, iv)

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Padding des données
    padded_data = pad(plaintext, AES.block_size)

    # Crypter les données
    ciphertext = cipher.encrypt(padded_data)

    # Écrire le IV et le ciphertext dans le fichier de sortie
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)

if __name__ == '__main__':
    input_file = 'db_config.json'  # Fichier à crypter
    output_file = 'db_config.enc'  # Fichier de sortie
    key = b'fd7fbf262118bc9631193efdab5e33adf88530610f7bc8bc7c19f7a3ca76f34d'  # Ta clé de 64 octets

    encrypt_file(input_file, output_file, key)
    print(f'Fichier {input_file} chiffré avec succès en {output_file}.')
