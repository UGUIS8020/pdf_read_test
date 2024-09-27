import os
import fitz  # PyMuPDF
import io
from PIL import Image

def extract_text_from_japanese_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def save_extracted_text(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def extract_images_from_pdf(pdf_path):
    images = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                images.append((image, f"page{i+1}_img{img_index+1}"))
    return images

def save_images(images, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for image, name in images:
        image.save(f"{output_dir}/{name}.png")

# 使用例
pdf_path = 'data/chapter01.pdf'  # あなたのPDFファイルのパスに置き換えてください
output_text_path = 'output/extracted_text.txt'
output_image_dir = 'output'

try:
    extracted_text = extract_text_from_japanese_pdf(pdf_path)
    save_extracted_text(extracted_text, output_text_path)
    print(f"テキストを {output_text_path} に保存しました。")

    images = extract_images_from_pdf(pdf_path)
    save_images(images, output_image_dir)
    print(f"{len(images)}枚の画像を {output_image_dir} ディレクトリに保存しました。")

except FileNotFoundError as e:
    print(f"エラー: ファイルまたはディレクトリが見つかりません。{e}")
except PermissionError as e:
    print(f"エラー: ファイルまたはディレクトリへのアクセス権限がありません。{e}")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")