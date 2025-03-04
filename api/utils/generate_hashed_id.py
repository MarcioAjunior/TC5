import hashlib
import random
import string

def generate_hashed_id(name: str) -> str:
    random_sequence = ''.join(random.choices(string.digits, k=10))
    
    input_string = name + random_sequence
    
    hashed_output = hashlib.sha256(input_string.encode()).hexdigest()
    
    return hashed_output
