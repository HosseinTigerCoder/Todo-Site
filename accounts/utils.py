import hashlib,time

def generate_token(email):
    text = email + str(time.time())
    return hashlib.sha256(text.encode()).hexdigest()