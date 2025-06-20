import pandas as pd
from datetime import datetime

class TranscriptParser:
    def __init__(self, file_path: str, cutoff_time: str = "09:05"):
        self.file_path = file_path
        self.cutoff_time = datetime.strptime(cutoff_time, "%H:%M")
        self.data = None
        self.attendance_records = []

    def load_csv(self):
        try:
            self.data = pd.read_csv(self.file_path)
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")

    def classify_attendance(self):
        if self.data is None:
            raise ValueError("CSV data not loaded. Call load_csv() first.")

        for _, row in self.data.iterrows():
            name = row["Name"]
            date = row["Date"]
            check_in = row["Check-In Time"]
            
            if pd.isna(check_in) or check_in == "-":
                status = "Absent"
            else:
                try:
                    check_in_time = datetime.strptime(check_in, "%H:%M")
                    if check_in_time <= self.cutoff_time:
                        status = "Present"
                    else:
                        status = "Late"
                except:
                    status = "Invalid Time Format"

            self.attendance_records.append({
                "Name": name,
                "Date": date,
                "Check-In Time": check_in,
                "Status": status
            })

    def get_attendance(self):
        return self.attendance_records
