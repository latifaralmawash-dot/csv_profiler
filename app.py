import streamlit as st
import pandas as pd
import json
import io
import csv
from pathlib import Path


from csv_profiler.profiler import profile_row, render_markdown


st.set_page_config(page_title="CSV Data Profiler", page_icon="", layout="wide")

st.title("CSV Data Profiler")
st.markdown("Upload a CSV file to generate an instant data profiling report.")


uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
   
    df = pd.read_csv(uploaded_file)
    
    st.subheader(" Data Preview (First 5 Rows)")
    st.dataframe(df.head())

   
    uploaded_file.seek(0)
    
  
    content = uploaded_file.getvalue().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    rows_data = list(reader)

    
    with st.spinner('Analyzing data...'):
     
        report = profile_row(rows_data)
        markdown_output = render_markdown(report)

    st.success("Analysis Complete!")

 
    tab1, tab2 = st.tabs([" Markdown Report", " Raw JSON Data"])
    
    with tab1:
        st.markdown(markdown_output)
        
    with tab2:
        st.json(report)

  
    st.divider()
    st.subheader(" Export Reports")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download Markdown Report",
            data=markdown_output,
            file_name="profiling_report.md",
            mime="text/markdown"
        )
        
    with col2:
        st.download_button(
            label="Download JSON Data",
            data=json.dumps(report, indent=4),
            file_name="profiling_data.json",
            mime="application/json"
        )
