import pandas as pd
import io
import os
import json
import re
from dotenv import load_dotenv
from langchain.schema import HumanMessage
from utils.llms import LLMModel2

load_dotenv()

class TranscriptParser:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file
        self.df = None
        self.attendance_df = None
        self.paragraph_text = None

        llm_model = LLMModel2()
        self.llm_model = llm_model.get_model2()

    def load_csv(self):
        if isinstance(self.uploaded_file, str):
            if "Name" in self.uploaded_file and "Remarks" in self.uploaded_file:
                self.df = pd.read_csv(io.StringIO(self.uploaded_file))
            elif self.uploaded_file.strip().startswith("Name,Remarks"):
                self.df = pd.read_csv(io.StringIO(self.uploaded_file))
            else:
                self.paragraph_text = self.uploaded_file
        else:
            filename = getattr(self.uploaded_file, 'name', '')
            if filename.endswith(".txt"):
                self.paragraph_text = self.uploaded_file.read().decode("utf-8")
            else:
                self.df = pd.read_csv(self.uploaded_file)

    def classify_attendance(self):
        if self.df is not None:
            statuses = []

            for _, row in self.df.iterrows():
                name = row.get("Name", "").strip()
                remark = str(row.get("Remarks", "")).strip()
                prompt = f"""
                    You are an intelligent attendance analyzer. Based on the remark below, classify the student as one of: Present, Late, Absent. Remark: "{remark}"
                    Answer with only one word: Present, Late, or Absent.
                """
                response = self.llm_model.invoke([HumanMessage(content=prompt)])
                prediction = response.content.strip().capitalize()

                if prediction not in ["Present", "Late", "Absent"]:
                    prediction = "Unknown"

                statuses.append({"Name": name, "Status": prediction})

            self.attendance_df = pd.DataFrame(statuses)

        elif self.paragraph_text is not None:
            prompt = f"""
                    You are an AI assistant. Read the following transcript and extract attendance information.
                    Transcript: \"\"\"{self.paragraph_text}\"\"\"
                    List each student's name and classify them as Present, Late, or Absent. Respond in JSON format as:
                    [{{ "Name": "Riya", "Status": "Present" }}, {{ "Name": "Rahul", "Status": "Late" }}]
                """

            response = self.llm_model.invoke([HumanMessage(content=prompt)])
            raw_text = response.content.strip()

            try:
                match = re.search(r"\[\s*{.*?}\s*\]", raw_text, re.DOTALL)
                if not match:
                    raise ValueError("No JSON array found in LLM response.")

                json_str = match.group(0)
                parsed = json.loads(json_str)

                df = pd.DataFrame(parsed)
                df.columns = [col.capitalize() for col in df.columns]
                self.attendance_df = df[["Name", "Status"]]

            except Exception as e:
                print("❌ Raw LLM Response:\n", raw_text)
                raise ValueError("Failed to parse LLM response as JSON.") from e

    def get_attendance(self):
        return self.attendance_df