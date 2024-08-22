from Crypto.Cipher import DES3
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad
import random
import os

# Diffie-Hellman Key Exchange
def diffie_hellman():
    # Public parameters
    P = 23  # Prime number
    g = 5   # Primitive root modulo P

    # User A's private key
    a = random.randint(1, P - 1)

    # User A computes public key
    A = (g ** a) % P

    # User B's private key
    b = random.randint(1, P - 1)

    # User B computes public key
    B = (g ** b) % P

    # Shared secret computation
    shared_secret_A = (B ** a) % P
    shared_secret_B = (A ** b) % P

    if shared_secret_A == shared_secret_B:
        return shared_secret_A
    else:
        raise Exception("Key exchange failed")

def encrypt_message(message, shared_secret):
    # Derive two 56-bit subkeys for Triple DES using scrypt with different salts
    key_1 = scrypt(shared_secret.to_bytes(16, byteorder='big'), salt=b'key1', key_len=8, N=2**14, r=8, p=1)
    key_2 = scrypt(shared_secret.to_bytes(16, byteorder='big'), salt=b'key2', key_len=8, N=2**14, r=8, p=1)

    # Generate an 8-byte initialization vector (IV)
    iv = os.urandom(8)  # Initialization vector

    # Create a Triple DES cipher in CBC mode with the concatenated keys and IV
    cipher = DES3.new(key_1 + key_2, DES3.MODE_CBC, iv)

    # Pad the message to a multiple of 8 bytes and encrypt it
    padded_message = pad(message.encode(), 8)
    ciphertext = cipher.encrypt(padded_message)

    # Return the IV concatenated with the ciphertext as the encrypted message
    return iv + ciphertext

def decrypt_message(ciphertext, shared_secret):
    # Derive two 56-bit subkeys for Triple DES using scrypt with different salts
    key_1 = scrypt(shared_secret.to_bytes(16, byteorder='big'), salt=b'key1', key_len=8, N=2**14, r=8, p=1)
    key_2 = scrypt(shared_secret.to_bytes(16, byteorder='big'), salt=b'key2', key_len=8, N=2**14, r=8, p=1)
    
    # Extract the 8-byte initialization vector (IV) from the ciphertext
    iv = ciphertext[:8]
    
    # Create a Triple DES cipher in CBC mode with the concatenated keys and IV
    cipher = DES3.new(key_1 + key_2, DES3.MODE_CBC, iv)
    
    # Decrypt the ciphertext, then remove padding and decode to get the original message
    decrypted_padded_message = cipher.decrypt(ciphertext[8:])
    original_message = unpad(decrypted_padded_message, 8).decode()
    
    # Return the decrypted original message
    return original_message



# Main function to demonstrate secure communication using Diffie-Hellman and Triple DES
def main():
    
    # Perform Diffie-Hellman key exchange to get a shared secret
    shared_secret = diffie_hellman()

 

    # Message to be sent from User A to User B
    user_a_message = "Hello from User A!"
    
    # Encrypt the message using 3DES and the generated encryption key
    encrypted_message = encrypt_message(user_a_message, shared_secret)
    
    # Print the original message, encrypted message, and perform decryption
    print("User A: Original Message -", user_a_message)
    print("User A: Encrypted Message -", encrypted_message)

    # Decrypt the encrypted message using the encryption key
    decrypted_message = decrypt_message(encrypted_message, shared_secret)
    print("User B: Decrypted Message -", decrypted_message)


if __name__ == "__main__":
    main()