from pathlib import Path
from PyPDF2 import PdfMerger

def merge_pdf_files(folder_path, output_file):
    folder = Path(folder_path)
    merger = PdfMerger()

    # フォルダ内のPDFファイルをリストアップし、番号順にソート
    pdf_files = sorted(
        [f for f in folder.glob("*.pdf") if f.name[0].isdigit()],
        key=lambda x: int(x.name.split('_')[0])
    )

    # ファイル数の確認
    if len(pdf_files) != 66:
        print(f"警告: フォルダ内に66個のPDFファイルがありません。実際のファイル数: {len(pdf_files)}")

    # PDFファイルを順番に統合
    for pdf_file in pdf_files:
        merger.append(str(pdf_file))
        print(f"追加: {pdf_file.name}")

    # 統合したPDFを保存
    with open(output_file, "wb") as output:
        merger.write(output)

    print(f"PDFファイルの統合が完了しました。出力ファイル: {output_file}")

# スクリプトの実行
if __name__ == "__main__":
    folder_path = r"C:\Users\jinen\AppData\Local\Temp\Brother.iPS\Temp\ScanToApp\test"
    output_file = "merged_output.pdf"
    merge_pdf_files(folder_path, output_file)