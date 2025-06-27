# nodes/pgw_node.py
import datetime
import random
from utils import generate_egyptian_number, get_or_create_session_id

class PGWNode:
    def generate_cdr(self, session_map):
        cdr_type = "data"
        cdr_id = random.randint(1000000, 9999999)
        timestamp = datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, 86400))
        timestamp_str = timestamp.strftime("%Y/%m/%d %H:%M:%S")

        party_a = generate_egyptian_number()
        apn = f"apn{random.randint(1,5)}.internet"
        volume_kb = random.randint(1000, 50000)
        cost = round(volume_kb * 0.0002, 2)

        session_id = get_or_create_session_id(cdr_type, party_a, apn, session_map)

        return [cdr_id, cdr_type, "PGW", party_a, apn, timestamp_str, "", volume_kb, cost, session_id]
