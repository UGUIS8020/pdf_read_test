import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, output_folder):
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # PDFファイルを読み込む
    pdf = PdfReader(input_path)

    # 各ページを個別のPDFファイルとして保存
    for page_num in range(len(pdf.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page_num])

        output_filename = f'page_{page_num + 1}.pdf'
        output_path = os.path.join(output_folder, output_filename)

        # 新しいPDFファイルを保存
        with open(output_path, 'wb') as out:
            pdf_writer.write(out)

        print(f'Saved {output_filename}')

# スクリプトを実行
if __name__ == "__main__":
    input_pdf = "data/input.pdf"  # 入力PDFファイルのパス
    output_folder = "output_pages"  # 出力フォルダのパス

    split_pdf(input_pdf, output_folder)
    print("PDF splitting completed.")