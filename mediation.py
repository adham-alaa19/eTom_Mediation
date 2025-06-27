import time
from pathlib import Path
import shutil
import csv

from Functions.convert import convert
from Functions.correlate import correlate
from Functions.normalize import normalize
from Functions.deduplicate import duplicate
from Functions.validate import validate
from Functions.guide import guide
from Functions.report import report

input_folder = Path("input")
processed_folder = Path("processed")
input_folder.mkdir(exist_ok=True)
processed_folder.mkdir(exist_ok=True)

def process_cdr_file(filepath: Path):
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = dict(row)
            try:
                record = convert(record)
                if duplicate(record):  # type: ignore
                    continue
                if not validate(record):  # type: ignore
                    continue
                record = normalize(record)
                record = correlate(record)
                record = guide(record)
                report(record)
            except Exception as e:
                print(f"⚠️ Failed to process record: {e}")
                continue

    shutil.move(filepath, processed_folder / filepath.name)
    print(f"✅ Processed: {filepath.name}")

def main():
    print("Starting CDR processor. Monitoring input folder every 10 seconds...")
    while True:
        files = list(input_folder.glob("cdr_mix_*.csv"))
        if files:
            for file in files:
                process_cdr_file(file)
        else:
            print("No files found. Waiting...")
        time.sleep(10)

if __name__ == "__main__":
    main()
