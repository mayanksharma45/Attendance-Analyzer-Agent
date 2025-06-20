import pandas as pd
import os

class AttendanceSaver:
    def __init__(self, output_dir: str = "data", output_file: str = "final_attendance.csv"):
        self.output_dir = output_dir
        self.output_file = output_file
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, attendance_list: list):
        if not attendance_list or not isinstance(attendance_list, list):
            raise ValueError("Attendance list is empty or not in valid format.")

        df = pd.DataFrame(attendance_list)
        output_path = os.path.join(self.output_dir, self.output_file)
        df.to_csv(output_path, index=False)
        print(f"[✔] Attendance saved to: {output_path}")
        return output_path
