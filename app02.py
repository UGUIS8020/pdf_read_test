from pdfminer.high_level import extract_text
import re

def extract_text_from_japanese_pdf(pdf_path):
    # PDFからテキストを抽出
    text = extract_text(pdf_path)
    
    # 不要な空白や改行を削除
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# 使用例
pdf_path = 'data/chapter01.pdf'  # あなたのPDFファイルのパスに置き換えてください
extracted_text = extract_text_from_japanese_pdf(pdf_path)
print(extracted_text)