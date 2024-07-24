import os
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

# Set your endpoint and key variables
endpoint = "https://documentanalysiseswar.cognitiveservices.azure.com/"
key = "4b916a1b09ca451c985fa308044880ee"

# Helper functions
def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (
            word.span.offset + word.span.length
        ) <= (span.offset + span.length):
            return True
    return False

def analyze_layout(formUrl):
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read", AnalyzeDocumentRequest(url_source=formUrl)
    )

    result: AnalyzeResult = poller.result()

    output = {
        "handwritten_content": "Document contains handwritten content" if result.styles and any([style.is_handwritten for style in result.styles]) else "Document does not contain handwritten content",
        "pages": [],
        "tables": []
    }

    for page in result.pages:
        page_info = {
            "page_number": page.page_number,
            "width": page.width,
            "height": page.height,
            "unit": page.unit,
            "lines": [],
            "selection_marks": []
        }

        if page.lines:
            for line_idx, line in enumerate(page.lines):
                words = get_words(page, line)
                line_info = {
                    "line_index": line_idx,
                    "word_count": len(words),
                    "text": line.content,
                    "bounding_polygon": line.polygon,
                    "words": [{"word": word.content, "confidence": word.confidence} for word in words]
                }
                page_info["lines"].append(line_info)

        if page.selection_marks:
            page_info["selection_marks"] = [
                {
                    "state": selection_mark.state,
                    "bounding_polygon": selection_mark.polygon,
                    "confidence": selection_mark.confidence
                }
                for selection_mark in page.selection_marks
            ]

        output["pages"].append(page_info)

    if result.tables:
        for table_idx, table in enumerate(result.tables):
            table_info = {
                "table_index": table_idx,
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": [],
                "bounding_regions": [
                    {"page_number": region.page_number, "polygon": region.polygon}
                    for region in table.bounding_regions
                ] if table.bounding_regions else []
            }
            for cell in table.cells:
                cell_info = {
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "text": cell.content,
                    "bounding_regions": [
                        {"page_number": region.page_number, "polygon": region.polygon}
                        for region in cell.bounding_regions
                    ] if cell.bounding_regions else []
                }
                table_info["cells"].append(cell_info)

            output["tables"].append(table_info)

    return output

# Streamlit UI
def main():
    st.title("Document Analysis with Azure Document Intelligence")

    formUrl = st.text_input("Enter the document URL:")

    if st.button("Analyze Document"):
        if formUrl:
            st.write("Analyzing document...")
            output = analyze_layout(formUrl)
            
            st.subheader("Handwritten Content Status")
            st.write(output["handwritten_content"])
            
            for page in output["pages"]:
                st.subheader(f"Page #{page['page_number']}")
                st.write(f"Width: {page['width']} {page['unit']}, Height: {page['height']} {page['unit']}")
                
                if page["lines"]:
                    st.write("### Lines")
                    for line in page["lines"]:
                        st.write(f"Line #{line['line_index']}:")
                        st.write(f"Text: {line['text']}")
                        st.write(f"Word Count: {line['word_count']}")
                        st.write(f"Bounding Polygon: {line['bounding_polygon']}")
                        st.write("Words:")
                        for word in line["words"]:
                            st.write(f"  - {word['word']} (Confidence: {word['confidence']})")

                if page["selection_marks"]:
                    st.write("### Selection Marks")
                    for mark in page["selection_marks"]:
                        st.write(f"State: {mark['state']}")
                        st.write(f"Bounding Polygon: {mark['bounding_polygon']}")
                        st.write(f"Confidence: {mark['confidence']}")

            if output["tables"]:
                st.subheader("Tables")
                for table in output["tables"]:
                    st.write(f"Table #{table['table_index']}")
                    st.write(f"Rows: {table['row_count']}, Columns: {table['column_count']}")
                    
                    if table["bounding_regions"]:
                        st.write("Bounding Regions:")
                        for region in table["bounding_regions"]:
                            st.write(f"  - Page: {region['page_number']}, Polygon: {region['polygon']}")
                    
                    if table["cells"]:
                        st.write("Cells:")
                        for cell in table["cells"]:
                            st.write(f"Cell[{cell['row_index']}][{cell['column_index']}]")
                            st.write(f"Text: {cell['text']}")
                            if cell["bounding_regions"]:
                                st.write("Bounding Regions:")
                                for region in cell["bounding_regions"]:
                                    st.write(f"  - Page: {region['page_number']}, Polygon: {region['polygon']}")

        else:
            st.error("Please enter a valid document URL")

if __name__ == "__main__":
    main()
