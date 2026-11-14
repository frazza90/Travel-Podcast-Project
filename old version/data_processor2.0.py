import os
import pdfplumber
import pandas as pd

# --- Define the Two Local PDF Paths ---
pdf_path_1 = r"C:\Users\Helen\Desktop\Chris Ironhack\Week 4\Lesson 3\hong-kong-neighbourhoods.pdf"
pdf_path_2 = r"C:\Users\Helen\Desktop\Chris Ironhack\Week 4\Lesson 3\Hong Kong – Travel guide at Wikivoyage.pdf"

def extract_pdf_data(path, source_label):
    """Extracts text page by page from a local PDF and returns a structured DataFrame."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file was not found at: {path}")
    
    extracted_data = []
    with pdfplumber.open(path) as pdf:
        print(f"Successfully opened [{source_label}]. Total pages: {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                cleaned_text = text.strip()
                extracted_data.append({
                    "source": source_label,
                    "identifier": f"Page {i + 1}",
                    "raw_text": cleaned_text,
                    "character_count": len(cleaned_text)
                })
    return pd.DataFrame(extracted_data)

def load_master_dataset():
    """Executes the ingestion pipeline for all sources and combines them into df_master."""
    print("--- Processing Source 1 ---")
    df_pdf_1 = extract_pdf_data(pdf_path_1, "Neighbourhoods PDF")

    print("\n--- Processing Source 2 ---")
    df_pdf_2 = extract_pdf_data(pdf_path_2, "Wikivoyage PDF")

    df_master = pd.concat([df_pdf_1, df_pdf_2], ignore_index=True)
    
    print(f"\n--- Master Dataset Ready ---")
    print(f"Total entries across all sources: {len(df_master)}")
    print("Breakdown by source:")
    print(df_master["source"].value_counts())
    
    return df_master


def test_master_data_organization(df):
    """Runs automated sanity checks on the master dataset schema and contents."""
    print("\n--- Running Master Data Organization Tests ---")
    
    assert not df.empty, "Test Failed: The DataFrame is completely empty!"
    print("✓ Test 1 Passed: Master DataFrame contains rows.")

    expected_columns = {"source", "identifier", "raw_text", "character_count"}
    assert expected_columns.issubset(df.columns), f"Test Failed: Missing expected columns. Found: {df.columns.tolist()}"
    print("✓ Test 2 Passed: All required multi-source columns are present.")

    empty_rows = df[df["character_count"] == 0]
    if not empty_rows.empty:
        print(f"⚠️ Warning: Found {len(empty_rows)} empty row(s) from sources: {empty_rows['source'].unique().tolist()}")
    else:
        print("✓ Test 3 Passed: No empty text rows detected.")

    assert pd.api.types.is_string_dtype(df["source"]), "Test Failed: 'source' must be string type."
    assert pd.api.types.is_string_dtype(df["identifier"]), "Test Failed: 'identifier' must be string type."
    assert pd.api.types.is_string_dtype(df["raw_text"]), "Test Failed: 'raw_text' must be string type."
    assert df["character_count"].dtype in [int, "int64"], "Test Failed: 'character_count' must be integer type."
    print("✓ Test 4 Passed: All column data types are correct.")

    sources_found = df["source"].unique().tolist()
    print(f"✓ Test 5 Passed: Detected sources in dataset: {sources_found}")
    print("\n--- All master data tests completed successfully! ---")


# Execute data loading, testing, and EDA only when running this file directly
if __name__ == "__main__":
    # 1. Load data
    df_master = load_master_dataset()
    
    # 2. Run automated test suite
    test_master_data_organization(df_master)
    
    # 3. Run Exploratory Data Analysis (EDA) inspections
    print("\n--- Character Count Summary Statistics ---")
    print(df_master["character_count"].describe())

    print("\nShortest entries:")
    print(df_master.nsmallest(3, "character_count")[["source", "identifier", "character_count"]])

    print("\nLongest entries:")
    print(df_master.nlargest(3, "character_count")[["source", "identifier", "character_count"]])

    target_identifier = "Page 2"
    text_sample = df_master.loc[df_master["identifier"] == target_identifier, "raw_text"].values[0]
    print(f"\n--- Preview of {target_identifier} ---")
    print(text_sample[:500] + "...")