import os
import fitz
import json
from PIL import Image
import io

def extract_structured_content(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    structured_content = []
    
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            page_content = {"page": page_num + 1, "text": "", "images": []}
            
            # テキスト抽出
            page_content["text"] = page.get_text()
            
            # 画像抽出
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                
                # 画像の保存
                image_filename = f"page{page_num + 1}_img{img_index + 1}.png"
                image.save(os.path.join(output_dir, image_filename))
                
                # 画像情報の記録
                page_content["images"].append({
                    "filename": image_filename,
                    "width": image.width,
                    "height": image.height
                })
            
            structured_content.append(page_content)
    
    # 構造化されたコンテンツをJSONファイルとして保存
    with open(os.path.join(output_dir, "structured_content.json"), "w", encoding="utf-8") as f:
        json.dump(structured_content, f, ensure_ascii=False, indent=2)

# 使用例
pdf_path = 'data/chapter01.pdf'  # あなたのPDFファイルのパスに置き換えてください
output_dir = 'output/structured_content'

try:
    extract_structured_content(pdf_path, output_dir)
    print(f"構造化されたコンテンツを {output_dir} に保存しました。")
except Exception as e:
    print(f"エラーが発生しました: {e}")