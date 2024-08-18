from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from io import BytesIO
from PIL import Image
import fitz  # PyMuPDF
import tempfile


def merge_pdfs_two_up(folder_path, output_file):
    folder = Path(folder_path)

    # フォルダ内のPDFファイルをリストアップし、番号順にソート
    pdf_files = sorted(
        [f for f in folder.glob("*.pdf") if f.name[0].isdigit()],
        key=lambda x: int(x.name.split('_')[0])
    )

    # ファイル数の確認
    if len(pdf_files) != 66:
        print(f"警告: フォルダ内に66個のPDFファイルがありません。実際のファイル数: {len(pdf_files)}")

    output = PdfWriter()

    # PDFページを画像に変換する関数
    def pdf_page_to_image(pdf_path):
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # 最初のページを取得
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img

    with tempfile.TemporaryDirectory() as tmpdirname:
        for i in range(0, len(pdf_files), 2):
            # 2つのPDFファイルを読み込む
            pdf1_path = pdf_files[i]
            pdf2_path = pdf_files[i + 1] if i + 1 < len(pdf_files) else None

            # 新しい空のPDFページを作成
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=landscape(letter))
            width, height = landscape(letter)

            # 偶数ページ（左側）を配置
            if pdf2_path:
                page2_image = pdf_page_to_image(pdf2_path)
                temp_image_path = Path(tmpdirname) / f"temp_image2_{i}.png"
                page2_image.save(temp_image_path)
                can.drawImage(str(temp_image_path), 0, 0, width / 2, height)

            # 奇数ページ（右側）を配置
            page1_image = pdf_page_to_image(pdf1_path)
            temp_image_path = Path(tmpdirname) / f"temp_image1_{i}.png"
            page1_image.save(temp_image_path)
            can.drawImage(str(temp_image_path), width / 2, 0, width / 2, height)

            can.save()

            # 新しいページを出力PDFに追加
            packet.seek(0)
            new_page = PdfReader(packet).pages[0]
            output.add_page(new_page)

            print(f"処理: {'偶数ページ ' + pdf2_path.name if pdf2_path else '(空白)'} と 奇数ページ {pdf1_path.name}")

    # 統合したPDFを保存
    output_path = Path(output_file)
    with output_path.open("wb") as f:
        output.write(f)

    print(f"PDFファイルの統合が完了しました。出力ファイル: {output_path}")


# スクリプトの実行
if __name__ == "__main__":
    folder_path = Path(r"C:\Users\jinen\AppData\Local\Temp\Brother.iPS\Temp\ScanToApp\test")
    output_file = "merged_two_up_output.pdf"
    merge_pdfs_two_up(folder_path, output_file)  # この行から '=' を削除しました