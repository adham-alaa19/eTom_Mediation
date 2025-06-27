import random
import uuid

def generate_egyptian_number():
    prefix = random.choice(["10", "11", "12"])
    number = random.randint(1000000, 9999999)
    return f"+20{prefix}{number}"

def get_or_create_session_id(cdr_type, party_a, party_b_or_apn, session_map):
    reuse_probability = {"data": 0.9, "voice": 0.3, "sms": 0.05}
    key = (cdr_type, party_a) if cdr_type == "data" else (cdr_type, party_a, party_b_or_apn)
    if key in session_map and random.random() < reuse_probability[cdr_type]:
        return session_map[key]
    session_id = str(uuid.uuid4())
    session_map[key] = session_id
    return session_id
