import threading
import queue
import math
import time
from ctypes import c_ubyte

KEY_LENGTH = 2
MAX_QUEUE_SIZE = math.pow(2,KEY_LENGTH * 8)
NUM_THREADS = 4  # Adjust based on your environment

# RC4 decryption function
def rc4_decrypt(input_bytes, key):
    bytes_result = bytes.fromhex(input_bytes)
    S = list(range(256))
    j = 0
    out = []

    # KSA Phase
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA Phase
    i = j = 0
    for char in bytes_result:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])

    return bytes(out)

# Function to convert a long integer to a byte array
def long_to_bytes(num):
    return num.to_bytes(KEY_LENGTH, 'little')
# Thread worker function
def worker(queue, ciphertext):
    while True:
        num = queue.get()
        if num == -1:
            break  # Exit condition

        key = long_to_bytes(num)
        decrypted_text = rc4_decrypt(ciphertext, key)

        if all(32 <= c < 127 for c in decrypted_text):
            print(f"Decrypted text with key {key}: {decrypted_text.decode()}")
            end = time.time()
            print("Time in seconds:", end - start)

        queue.task_done()

# Main function to set up threads and process the decryption
def main():
    # Example ciphertext (as bytes for simplicity)
    ciphertext = "7d7899a102039e3fa4b92c57e685d47ce3ded0cfc48f"  # Example, replace with actual ciphertext
    global start, end
    start = time.time()
    # Setting up queue
    q = queue.Queue(maxsize=MAX_QUEUE_SIZE)
    # Starting worker threads
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(q, ciphertext))
        t.start()
        threads.append(t)
    # Enqueue tasks
    bits = 8 * KEY_LENGTH
    limit =int(math.pow(2, bits))
    for num in range(limit):
        q.put(num)
    
    # Signal no more tasks
    for _ in range(NUM_THREADS):
        q.put(-1)

    # Wait for all tasks to be completed
    q.join()

    # Wait for all threads to finish
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()