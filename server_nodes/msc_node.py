# nodes/msc_node.py
import datetime
import random
from utils import generate_egyptian_number, get_or_create_session_id

class MSCNode:
    def generate_cdr(self, session_map):
        cdr_type = "voice"
        cdr_id = random.randint(1000000, 9999999)
        timestamp = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
        timestamp_str = timestamp.strftime("%d/%m/%Y %H:%M")  

        party_a = generate_egyptian_number()
        party_b = generate_egyptian_number()
        duration = round(random.uniform(1, 10), 2)
        cost = round(duration * 0.07, 2)

        session_id = get_or_create_session_id(cdr_type, party_a, party_b, session_map)

        return [cdr_id, cdr_type, "MSC", party_a, party_b, timestamp_str, duration, "", cost, session_id]
