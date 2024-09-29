import os
import json
from PIL import Image
import shutil
import re

def process_png_files(input_folder, output_base_dir):
    os.makedirs(output_base_dir, exist_ok=True)
    
    content_structure = {}
    
    # ファイル名から情報を抽出する正規表現パターン
    pattern = re.compile(r'page(\d+)_(\d+)\.png')
    
    for filename in sorted(os.listdir(input_folder)):
        if filename.lower().endswith('.png'):
            match = pattern.match(filename)
            if match:
                page_num = int(match.group(1))
                image_num = int(match.group(2))
                
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_base_dir, filename)
                
                # 画像をコピー
                shutil.copy2(input_path, output_path)
                
                # 画像情報を取得
                with Image.open(input_path) as img:
                    width, height = img.size
                
                # ページ情報を更新
                if page_num not in content_structure:
                    content_structure[page_num] = {
                        "page": page_num,
                        "images": []
                    }
                
                content_structure[page_num]["images"].append({
                    "file": filename,
                    "width": width,
                    "height": height,
                    "image_number": image_num
                })
    
    # ページ番号でソートし、リストに変換
    sorted_content = [content_structure[page] for page in sorted(content_structure.keys())]
    
    # 構造情報をJSONファイルとして保存
    with open(os.path.join(output_base_dir, "content_structure.json"), "w", encoding="utf-8") as f:
        json.dump(sorted_content, f, ensure_ascii=False, indent=2)

# 使用例
input_folder = 'data/自家歯牙移植_増補新版_月星光博/png/contents'
output_base_dir = 'output/processed_content'

try:
    process_png_files(input_folder, output_base_dir)
    print(f"処理されたコンテンツを {output_base_dir} に保存しました。")
except Exception as e:
    print(f"エラーが発生しました: {e}")