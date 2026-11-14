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

if __name__ == "__main__":
    load_master_dataset()