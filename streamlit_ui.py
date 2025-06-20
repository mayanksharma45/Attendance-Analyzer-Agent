import streamlit as st
from toolkit.parser import TranscriptParser
from utils.updater import AttendanceSaver
from agent import build_agent

st.set_page_config(page_title="Attendance Analyzer", layout="centered")
st.title("📊 AI-Powered Attendance Analyzer Agent")

# Upload section
uploaded_file = st.file_uploader("📁 Upload Attendance CSV", type=["csv"])

if uploaded_file:
    st.success("✅ File uploaded!")

    # Parse and classify attendance
    parser = TranscriptParser(uploaded_file)
    parser.load_csv()
    parser.classify_attendance()
    attendance = parser.get_attendance()

    # Display parsed data
    st.subheader("📋 Classified Attendance")
    st.dataframe(attendance, use_container_width=True)

    # Save to CSV
    saver = AttendanceSaver()
    saved_path = saver.save(attendance)

    # Run LangGraph agent
    st.subheader("🧠 AI Summary")
    graph = build_agent()
    state = {"messages": [{"role": "user", "content": attendance}]}
    final_state = graph.invoke(state)
    st.info(final_state['messages'][-1]['content'])

    st.success("✅ Attendance processing complete!")
