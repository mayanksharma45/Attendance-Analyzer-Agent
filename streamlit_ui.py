import streamlit as st
from langchain_core.messages import HumanMessage
from agent import AttendanceAnalyzerAgent
import pandas as pd
import os

OUTPUT_PATH = "attendance_sheet.xlsx"

st.set_page_config(page_title="AI Attendance Analyzer", layout="centered")
st.title("AI-Powered Attendance Analyzer Agent")

uploaded_file = st.file_uploader("📁 Upload Attendance Transcript (.txt or .csv)", type=["txt", "csv"])

agent = AttendanceAnalyzerAgent()
app = agent.build()

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")

    if st.button("Analyze Attendance"):
        with st.spinner("Analyzing... ⏳"):
            try:
                messages = [HumanMessage(content=file_content)]

                app.invoke({"messages": messages})

                if os.path.exists(OUTPUT_PATH):
                    df = pd.read_excel(OUTPUT_PATH)

                    st.subheader("📋 Classified Attendance Sheet")
                    st.dataframe(df, use_container_width=True)

                    with open(OUTPUT_PATH, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Attendance Sheet",
                            data=f,
                            file_name="attendance_sheet.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                st.success("✅ Attendance analysis completed.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("📌 Please upload a transcript or CSV file to start.")
