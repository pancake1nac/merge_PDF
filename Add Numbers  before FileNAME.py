from pathlib import Path


def rename_files_with_numbers(folder_path):
    # Pathオブジェクトを作成
    folder = Path(folder_path)

    # フォルダ内のファイルをリストアップし、ソートする
    files = sorted(file for file in folder.iterdir() if file.is_file())

    # 66個のファイルがあることを確認
    if len(files) != 66:
        print(f"警告: フォルダ内に66個のファイルがありません。実際のファイル数: {len(files)}")

    # ファイルに番号を付けてリネーム
    for index, file in enumerate(files, start=1):
        # 新しいファイル名を生成>
        new_filename = f"{index:02d}_{file.name}"

        # 新しいパスを作成
        new_file = file.with_name(new_filename)

        # ファイルをリネーム
        file.rename(new_file)
        print(f"リネーム: {file.name} -> {new_filename}")


# スクリプトの実行
folder_path = r"C:\Users\jinen\AppData\Local\Temp\Brother.iPS\Temp\ScanToApp\test"
rename_files_with_numbers(folder_path)
print("ファイルの番号付けが完了しました。")