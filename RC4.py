def swap_bytes(a, b):
    """Swaps the values of two bytes."""
    a, b = b, a

def create_sbox(key):
    """Initializes the S-box using the provided key."""
    sbox = list(range(256))
    j = 0
    for i in range(256):
        j = (j + sbox[i] + key[i % len(key)]) % 256
        swap_bytes(sbox[i], sbox[j])
    return sbox

def rc4_encrypt(data, key):
    """Encrypts the data using the RC4 algorithm."""
    sbox = create_sbox(key)
    i = 0
    j = 0
    ciphertext = bytearray(len(data))
    for k in range(len(data)):
        i = (i + 1) % 256
        j = (j + sbox[i]) % 256
        swap_bytes(sbox[i], sbox[j])
        t = (sbox[i] + sbox[j]) % 256
        ciphertext[k] = data[k] ^ sbox[t]
    return ciphertext

# Example usage (remember, RC4 is insecure)
plaintext = b"This is a sample"
key = b"INTR"
ciphertext = rc4_encrypt(plaintext, key)

print("Plaintext:", plaintext.decode())
print("Ciphertext:", ciphertext.hex())  # Print ciphertext in hexadecimal format

# Decryption is identical to encryption, using the same key and ciphertext
decrypted_text = rc4_encrypt(ciphertext, key)
print("Decrypted Text:", decrypted_text.decode())
