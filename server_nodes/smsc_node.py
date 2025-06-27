# nodes/smsc_node.py
import datetime
import random
from utils import generate_egyptian_number, get_or_create_session_id

class SMSCNode:
    def generate_cdr(self, session_map):
        cdr_type = "sms"
        cdr_id = random.randint(1000000, 9999999)
        timestamp = int(datetime.datetime.now().timestamp())  # SMSC uses epoch

        party_a = generate_egyptian_number()
        party_b = generate_egyptian_number()
        cost = round(random.uniform(0.1, 0.5), 2)

        session_id = get_or_create_session_id(cdr_type, party_a, party_b, session_map)

        return [cdr_id, cdr_type, "SMSC", party_a, party_b, timestamp, "", "", cost, session_id]
