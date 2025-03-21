from src.external.ocr.textract import Textract

if __name__ == "__main__":
    scanner = Textract()
    result = scanner.extract_raw_text("s3://document-extractor-gsa-dev-documents/test_dd214.jpg")

    print(f"Raw text is {result}")
