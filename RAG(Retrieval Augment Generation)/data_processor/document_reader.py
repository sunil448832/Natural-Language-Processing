from pathlib import Path
import pypdf  
import docx2txt 

class DocumentReader:
    @staticmethod
    def read_pdf(data_path):
        with open(data_path, "rb") as fp:
            pdf = pypdf.PdfReader(fp)  # Open the PDF file
            num_pages = len(pdf.pages)  # Get the number of pages in the PDF
            docs = []
            for page in range(num_pages):
                page_text = pdf.pages[page].extract_text()  # Extract text from the page
                page_label = pdf.page_labels[page]  # Get page label (e.g., page number)
                metadata = {"page_label": page_label, "file_name": data_path.name}
                docs.append({"text": page_text, "metadata": metadata})
            return docs

    @staticmethod
    def read_docx(data_path):
        metadata = {"file_name": data_path.name}
        doc = docx2txt.process(data_path)  # Extract text from the DOCX file
        docs = [{'text': doc, 'metadata': metadata}]
        return docs

    @staticmethod
    def read_txt(data_path):
        print(data_path.name)
        with open(data_path, "r") as fp:
            text = fp.read()  # Read text from the TXT file
            metadata = {"file_name": data_path.name}
            docs = [{'text': text, 'metadata': metadata}]
        return docs

    @staticmethod
    def read_document(file_path):
        data_path = Path(file_path)
        if data_path.suffix == ".pdf":
            return DocumentReader.read_pdf(data_path)  # Read PDF document
        elif data_path.suffix == ".docx":
            return DocumentReader.read_docx(data_path)  # Read DOCX document
        elif data_path.suffix == ".txt":
            return DocumentReader.read_txt(data_path)  # Read TXT document
        else:
            raise ValueError("Unsupported file format")

if __name__=='__main__':
    # Example usage:
    DATA_PATH = '71763-gale-encyclopedia-of-medicine.-vol.-1.-2nd-ed.pdf'
    documents = DocumentReader.read_document(DATA_PATH)  # Read the specified document
    print(documents)  # Print the extracted text and metadata
