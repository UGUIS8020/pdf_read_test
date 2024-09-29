import os
import json
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re

def preprocess_image(image_path):
    # 画像を読み込み
    img = cv2.imread(image_path)
    
    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ノイズ除去
    denoised = cv2.fastNlMeansDenoising(gray)
    
    # コントラスト調整
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    contrasted = clahe.apply(denoised)
    
    # シャープニング
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(contrasted, -1, kernel)
    
    return Image.fromarray(sharpened)

def process_png_files(input_folder, output_base_dir):
    os.makedirs(output_base_dir, exist_ok=True)
    
    content_structure = {}
    
    pattern = re.compile(r'page(\d+)_(\d+)\.png')
    
    for filename in sorted(os.listdir(input_folder)):
        if filename.lower().endswith('.png'):
            match = pattern.match(filename)
            if match:
                page_num = int(match.group(1))
                image_num = int(match.group(2))
                
                input_path = os.path.join(input_folder, filename)
                
                # 画像の前処理
                preprocessed_img = preprocess_image(input_path)
                
                # OCRを実行（複数の設定を試す）
                text_results = []
                for psm in [3, 4, 6]:  # 異なるページセグメンテーションモードを試す
                    text = pytesseract.image_to_string(
                        preprocessed_img, 
                        lang='jpn+eng',  # 日本語と英語の両方を認識
                        config=f'--psm {psm} --oem 1'
                    )
                    text_results.append(text.strip())
                
                # 最も長い結果を採用（通常、より多くのテキストが認識できた結果が良い）
                best_text = max(text_results, key=len)
                
                # ページ情報を更新
                if page_num not in content_structure:
                    content_structure[page_num] = {
                        "page": page_num,
                        "images": []
                    }
                
                content_structure[page_num]["images"].append({
                    "file": filename,
                    "image_number": image_num,
                    "text": best_text
                })
                
                # テキストファイルとして保存
                text_filename = f"page{page_num:03d}_{image_num:02d}.txt"
                with open(os.path.join(output_base_dir, text_filename), "w", encoding="utf-8") as f:
                    f.write(best_text)
    
    # ページ番号でソートし、リストに変換
    sorted_content = [content_structure[page] for page in sorted(content_structure.keys())]
    
    # 構造情報をJSONファイルとして保存
    with open(os.path.join(output_base_dir, "content_structure.json"), "w", encoding="utf-8") as f:
        json.dump(sorted_content, f, ensure_ascii=False, indent=2)

# 使用例
input_folder = 'data/自家歯牙移植_増補新版_月星光博'
output_base_dir = 'output/ocr_content'

try:
    process_png_files(input_folder, output_base_dir)
    print(f"OCR処理されたコンテンツを {output_base_dir} に保存しました。")
except Exception as e:
    print(f"エラーが発生しました: {e}")