import streamlit as st
import pandas as pd
from io import BytesIO
from rapidfuzz import fuzz, process
from functions import detect_fuzzy_duplicates_optimized

st.set_page_config(page_title="Duplicate Detector", layout="centered")

st.title("Duplicate Detector App")

st.markdown('The following App allows you to upload a csv file that you wish to check for duplicates within a single column, the output report will have the following structure:')
output_df_explanation=pd.DataFrame({
    'Index 1':['Row number in original file of record'],
    'Id column':['Column chosen as ID from original file (e.g. Part Number)'],
    'Column to check':['Column to analyze for duplicates'],
    'Index_2':['Matching row number from original file'],
    'Id column':['Matching ID (e.g. Part number)'],
    'Mathchin record':['Matching record value'],
    'Similarity':['Similarity percentage']
    })

st.dataframe(output_df_explanation)

# Step 1: Upload CSV
st.markdown("#### 1.Upload a CSV file")
uploaded_file = st.file_uploader("Upload a CSV file",type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully")

    # Step 2: Choose a column to analyse and for reference
    st.markdown("#### 2.Select the column to check for duplicates")
    column_to_check = st.selectbox("Choose a column from the list", df.columns)
    #Choose ID reference column
    st.markdown("#### 3. ***OPTIONAL*** - Select an ID reference column, otherwise choose the same column as above")
    id_column = st.selectbox("Choose an id column from the list (e.g. Part Number)", df.columns)

    # Step 3: Set similarity threshold
    st.markdown("#### 4. Select similarity threshold (%)")
    threshold = st.slider("Use the slider to select a similarity threshold", min_value=70, max_value=100, value=85)

    # Step 4: Run deduplication
    if st.button("Run Duplicate Check"):
        st.info("🔄 Processing...")

        result_df=detect_fuzzy_duplicates_optimized(df,column_to_check,id_column,threshold=threshold)
       
        # Step 5: Provide downloadable Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            result_df.to_excel(writer, index=False, sheet_name="Duplicates")
        output.seek(0)

        st.success("✅ Duplicate check completed")
        st.download_button("📥 Download Result Excel", output, file_name="duplicates_result.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
