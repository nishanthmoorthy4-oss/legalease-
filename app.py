import streamlit as st
import requests
from docx import Document
from fpdf import FPDF


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Generate professional legal documents using Generative AI."
)


# --------------------------------------------------
# INPUTS
# --------------------------------------------------

document_type = st.selectbox(
    "Document Type",
    [
        "Employment Agreement",
        "Lease Agreement",
        "Non-Disclosure Agreement (NDA)",
        "Service Agreement"
    ]
)


parties = st.text_area(
    "Parties",
    placeholder="Example: ABC Company and John"
)


terms = st.text_area(
    "Important Terms",
    placeholder="Example: Monthly salary, working hours, responsibilities..."
)


dates = st.text_input(
    "Dates",
    placeholder="Example: Effective from October 1, 2026"
)


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if st.button("Generate Document"):

    if not parties or not terms or not dates:

        st.warning("Please fill all the fields.")

    else:

        data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json=data
            )

            if response.status_code == 200:

                result = response.json()

                st.success("Document generated successfully!")

                document = result["document"]


                # --------------------------------------------------
                # EDITABLE DOCUMENT
                # --------------------------------------------------

                edited_document = st.text_area(
                    "Edit Your Legal Document",
                    document,
                    height=600
                )


                # --------------------------------------------------
                # TXT DOWNLOAD
                # --------------------------------------------------

                st.download_button(
                    label="📄 Download TXT",
                    data=edited_document,
                    file_name="LegalEase_Document.txt",
                    mime="text/plain"
                )


                # --------------------------------------------------
                # DOCX DOWNLOAD
                # --------------------------------------------------

                doc = Document()

                doc.add_heading(
                    document_type,
                    level=1
                )

                for paragraph in edited_document.split("\n"):

                    doc.add_paragraph(paragraph)

                docx_path = "LegalEase_Document.docx"

                doc.save(docx_path)

                with open(docx_path, "rb") as file:

                    st.download_button(
                        label="📝 Download DOCX",
                        data=file,
                        file_name="LegalEase_Document.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )


                # --------------------------------------------------
                # PDF DOWNLOAD
                # --------------------------------------------------

                pdf = FPDF()

                pdf.set_auto_page_break(
                    auto=True,
                    margin=15
                )

                pdf.add_page()

                pdf.set_font(
                    "Arial",
                    size=12
                )

                for line in edited_document.split("\n"):

                    pdf.multi_cell(
                        0,
                        8,
                        line
                    )

                pdf_path = "LegalEase_Document.pdf"

                pdf.output(pdf_path)

                with open(pdf_path, "rb") as file:

                    st.download_button(
                        label="📕 Download PDF",
                        data=file,
                        file_name="LegalEase_Document.pdf",
                        mime="application/pdf"
                    )


            else:

                st.error(
                    f"Failed to generate document. "
                    f"Status code: {response.status_code}"
                )


        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )