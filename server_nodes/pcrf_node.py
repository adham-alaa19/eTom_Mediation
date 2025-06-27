# nodes/pcrf_node.py
import datetime
from pgw_node import PGWNode

class PCRFNode(PGWNode):
    def generate_cdr(self, session_map):
        row = super().generate_cdr(session_map)
        dt = datetime.datetime.strptime(row[5], "%Y/%m/%d %H:%M:%S")
        row[5] = dt.isoformat()
        row[2] = "PCRF"
        return row
