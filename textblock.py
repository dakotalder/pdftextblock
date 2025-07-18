import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

# === Streamlit App Configuration ===
st.set_page_config(page_title="PDF Text Extractor", layout="centered")
st.title("📄 Multi-PDF Text Extractor")
st.markdown("Upload one or more PDF files to extract and combine their text content.")

# === File Uploader ===
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# === Extract Text ===
def extract_text_from_uploaded_pdfs(files):
    combined_text = ""

    for file in files:
        try:
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                for page in doc:
                    combined_text += page.get_text()
        except Exception as e:
            st.warning(f"❌ Failed to read {file.name}: {e}")
    
    return combined_text

if uploaded_files:
    with st.spinner("Extracting text from uploaded PDFs..."):
        all_text = extract_text_from_uploaded_pdfs(uploaded_files)

    st.success("✅ Text extracted successfully!")
    st.text_area("📄 Combined Extracted Text", all_text, height=400)

    # === Download Text ===
    output = BytesIO()
    output.write(all_text.encode('utf-8'))
    output.seek(0)

    st.download_button(
        label="📥 Download Extracted Text",
        data=output,
        file_name="combined_text_output.txt",
        mime="text/plain"
    )
