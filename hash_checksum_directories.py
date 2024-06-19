# Script de checksum de dossiers
# Vincent RÉMON - v.remon@groupeonepoint.com
# mer. 19 juin 2024
#
# Utilisation :
# Remplacer "/path/to/directory" par le chemin du répertoire à surveiller.
# Remplacer "hash.txt" par le chemin complet du fichier hash.txt si nécessaire.
#

import os
import hashlib

# calculate_directory_hash: Parcourt tous les répertoires et sous-répertoires, et calcule le hash SHA-256 en incluant le chemin du fichier et le contenu de chaque fichier.
def calculate_directory_hash(directory_path):
    """Calculate the SHA-256 hash of a directory."""
    sha256_hash = hashlib.sha256()
    
    for root, dirs, files in os.walk(directory_path):
        for names in sorted(dirs + files):
            file_path = os.path.join(root, names)
            sha256_hash.update(file_path.encode('utf-8'))
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# read_existing_hash: Lit le hash existant à partir du fichier hash.txt.
def read_existing_hash(file_path):
    """Read the existing hash from the hash file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read().strip()
    return None

# write_new_hash: Écrit le nouveau hash dans le fichier hash.txt.
def write_new_hash(file_path, hash_value):
    """Write the new hash to the hash file."""
    with open(file_path, 'w') as f:
        f.write(hash_value)

# main
def main(directory_path, hash_file_path):
    new_hash = calculate_directory_hash(directory_path) # calcule le nouveau hash du répertoire
    old_hash = read_existing_hash(hash_file_path) # Cherche le précéden hash
    
    if old_hash is None:
        print("No existing hash found. Writing new hash to file.")
        write_new_hash(hash_file_path, new_hash)
    elif old_hash != new_hash:   # compare avec l'ancien hash - s'il existe
        print("ALERT: Hash values have changed!")   # notifie une alerte si les valeurs sont différentes.
        print(f"Old hash: {old_hash}")
        print(f"New hash: {new_hash}")
        write_new_hash(hash_file_path, new_hash)    # met à jour le fichier hash.txt avec le nouveau hash.
    else:
        print("Hash values are identical. No changes detected.")

if __name__ == "__main__":
    directory_to_monitor = "/path/to/directory"  # Replace with the directory you want to monitor
    hash_file = "hash.txt"  # Replace with the path to your hash file
    
    main(directory_to_monitor, hash_file)
