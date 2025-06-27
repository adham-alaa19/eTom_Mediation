# generate_cdr.py
import csv
import os
import random
from server_nodes.msc_node import MSCNode
from server_nodes.smsc_node import SMSCNode
from server_nodes.pgw_node import PGWNode
from server_nodes.pcrf_node import PCRFNode

def generate_cdr_file(total_records=40, folder="input"):
    os.makedirs(folder, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"cdr_mix_{ts}.csv")

    header = ["cdr_id", "type", "node", "party_a", "party_b_or_apn", "timestamp", "duration_min", "volume_KB", "cost", "session_id"]
    session_map = {}

    rows = []
    for _ in range(total_records):
        node_cls = random.choice([MSCNode, SMSCNode, PGWNode, PCRFNode])
        node = node_cls()
        rows.append(node.generate_cdr(session_map))

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"✅ CDR file generated with multiple server formats: {filename}")

if __name__ == "__main__":
    import datetime
    generate_cdr_file(40)
