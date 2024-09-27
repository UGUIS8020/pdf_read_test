
import PyPDF2
import pytesseract
from PIL import Image
import io

def extract_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page in reader.pages:
            # テキストの抽出
            text = page.extract_text()
            print("抽出されたテキスト:", text)
            
            # 画像の抽出
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        image = xObject[obj]
                        data = image._data
                        img = Image.open(io.BytesIO(data))
                        
                        # 画像からテキストを抽出 (OCR)
                        image_text = pytesseract.image_to_string(img, lang='jpn')
                        print("画像から抽出されたテキスト:", image_text)
                        
                        # 画像の保存
                        img.save(f'extracted_image_{obj}.png')

# 使用例
extract_from_pdf('input.pdf')