import streamlit as st
import pandas as pd
from io import BytesIO
from rapidfuzz import fuzz, process
from functions import detect_fuzzy_duplicates_optimized

st.set_page_config(page_title="Duplicate Detector", layout="centered")

st.title("Duplicate Detector App")

st.markdown('This app lets you upload a CSV file and choose one column to analyze for possible duplicate or similar entries.')
st.markdown('The output report will have the following columns:')

col1,col2=st.columns(2,gap="small")
col1, col2 = st.columns([2,6])

with col1:
    st.markdown("### Column")
    st.divider()
    st.markdown('Index 1')
    st.markdown('Id column 1')
    st.markdown('Column to check')
    st.markdown('Index 2')
    st.markdown('Id column 2')
    st.markdown('Mathching record')
    st.markdown('Similarity')
with col2:
    st.markdown("### Description")
    st.divider()
    st.markdown('Row number in original file of record')
    st.markdown('Column chosen as ID from original file (e.g. Part Number)')
    st.markdown('Column to analyze for duplicates')
    st.markdown('Matching row number from original file')
    st.markdown('Matching ID (e.g. Part number)')
    st.markdown('Matched duplicate record')
    st.markdown('Similarity percentage')

example_data = {
    "Index_1": [333, 1199, 927, 664, 80],
    "PART NUMBER_1": [1, 2, 3, 4, 5],
    "DESCRIPTION_1": [
        "FILTER, OIL, SPIN-ON LUBE, 5MICRON, 3-11/16IN OD DIA, 6-5/8IN LG",
        "VALVE, SOLENOID, SEALED, 3-WAY CONFIGURATION, PNEUMATIC OPERATED ACTUATOR",
        "CABLE, ELECTRICAL, STARTER, 60V, 4GA CONDUCTOR, COPPER CONDUCTOR, NYLON JACKET, PVC INSULATION, -58 TO 221DEG F, 25FT LG, BLACK/RED JACKET",
        "VALVE, PROTECTION",
        "KIT, UNIVERSAL JOINT"
    ],
    "Index_2": [334, 1203, 931, 666, 102],
    "PART NUMBER_2": [6, 7, 8, 9, 10],
    "DESCRIPTION_2": [
        "FILTER, OIL, SPIN-ON LUBE, 5MICRON, 3-11/16IN OD DIA, 6-5/8IN LG",
        "VALVE, SOLENOID, BRACKET, 3-WAY CONFIGURATION, PNEUMATIC OPERATED ACTUATOR",
        "CABLE, ELECTRICAL, STARTER, 60V, 2/0GA CONDUCTOR, COPPER CONDUCTOR, PVC INSULATION, -58 TO 221DEG F, 25FT LG, BLACK JACKET",
        "VALVE, BRAKE PROTECTION",
        "KIT, UNIVERSAL JOINT SNAP RING"
    ],
    "Similarity": [100, 93.87755102, 91.53846154, 85, 80]
}

df_example = pd.DataFrame(example_data)

st.markdown('##### Output Example:')
st.dataframe(df_example)

# Step 1: Upload CSV or Excel file
st.markdown("#### 1.Upload a CSV or Excel file")
uploaded_file = st.file_uploader(
    "Browse for a CSV or Excel file",type=["csv","xlsx","xls"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully")

        # Step 2: Choose a column to analyse and for reference
        st.markdown("#### 2. Select the column to check for duplicates")
        column_to_check = st.selectbox("Choose a column from the list", df.columns)

        # Choose ID reference column
        st.markdown("#### 3. ***OPTIONAL*** - Select an ID reference column, otherwise choose the same column as above")
        id_column = st.selectbox("Choose an id column from the list (e.g. Part Number)", df.columns)

        # Step 3: Set similarity threshold
        st.markdown("#### 4. Select similarity threshold (%)")
        threshold = st.slider("Use the slider to select a similarity threshold", min_value=70, max_value=100, value=85)

        # Step 4: Run deduplication
        if st.button("Run Duplicate Check"):
            st.info("🔄 Processing...")

            result_df = detect_fuzzy_duplicates_optimized(df, column_to_check, id_column, threshold=threshold)

            # Step 5: Provide downloadable Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                result_df.to_excel(writer, index=False, sheet_name="Duplicates")
            output.seek(0)

            st.success("✅ Duplicate check completed")
            st.download_button(
                "📥 Download Result Excel", 
                output, 
                file_name="duplicates_result.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")