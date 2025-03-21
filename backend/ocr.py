from src.external.ocr.textract import Textract
from src.forms.w2 import W2

if __name__ == "__main__":
    scanner = Textract()
    form = W2()
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_w2.jpg", queries=form.queries())

    for key, value in result.items():
        print(key)
        print(f"\t{value}")
