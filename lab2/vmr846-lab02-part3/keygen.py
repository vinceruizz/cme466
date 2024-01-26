from Crypto.Random import get_random_bytes

key = get_random_bytes(16)  # AES key for 128-bit encryption
with open("./publisher_encrypted/key.bin", "wb") as pub_key:
    pub_key.write(key)

with open("./subscriber_encrypted/key.bin", "wb") as sub_key:
    sub_key.write(key)
