from toolkit.parser import TranscriptParser
from utils.updater import AttendanceSaver
import pandas as pd
import json

from toolkit.parser import TranscriptParser
from utils.updater import AttendanceSaver
import pandas as pd
from io import StringIO
import json

def parse_transcript_tool_func(file_content: str) -> str:
    parser = TranscriptParser(file_content)
    parser.load_csv()
    parser.classify_attendance()
    df = parser.get_attendance()
    return json.dumps(df.to_dict(orient="records"))

def update_sheet_tool_func(attendance_json: str) -> str:
    try:
        json.loads(attendance_json)
        df = pd.read_json(StringIO(attendance_json))
    except Exception as e:
        return f"Error: {str(e)}\nPlease fix your mistakes."

    saver = AttendanceSaver()
    path = saver.save(df)
    return f"✅ Sheet updated and saved at: {path}"
    


