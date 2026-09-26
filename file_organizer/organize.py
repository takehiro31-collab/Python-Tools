"""フォルダの中のファイルを、種類ごとのフォルダに自動で振り分けるツール。

使い方:
    python organize.py フォルダの場所            # まずは確認だけ（ファイルは動かさない）
    python organize.py フォルダの場所 --run      # 実際に振り分ける
"""

import argparse
import sys
from pathlib import Path

# 拡張子（ファイル名の最後の .jpg など）と、振り分け先フォルダ名の対応表。
# ここに行を足せば、好きな種類を増やせます。
CATEGORIES = {
    "画像": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".svg"],
    "文書": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"],
    "表計算": [".xls", ".xlsx", ".csv", ".ods"],
    "スライド": [".ppt", ".pptx", ".key", ".odp"],
    "動画": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm"],
    "音楽": [".mp3", ".wav", ".m4a", ".aac", ".flac"],
    "圧縮ファイル": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "インストーラー": [".exe", ".msi", ".dmg", ".pkg"],
}
OTHER = "その他"


def category_for(path):
    """ファイルの拡張子から、振り分け先のフォルダ名を決める。"""
    ext = path.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return OTHER


def unique_destination(dest):
    """同じ名前のファイルがすでにあるときは「名前 (2).jpg」のように番号を付ける。"""
    if not dest.exists():
        return dest
    n = 2
    while True:
        candidate = dest.with_name(f"{dest.stem} ({n}){dest.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def plan_moves(folder):
    """どのファイルをどこへ動かすかの一覧を作る（まだ動かさない）。"""
    moves = []
    for path in sorted(folder.iterdir()):
        # フォルダや、隠しファイル（.DS_Store など）は触らない
        if not path.is_file() or path.name.startswith("."):
            continue
        moves.append((path, folder / category_for(path) / path.name))
    return moves


def organize(folder, run=False):
    """振り分けを実行する。run=False のときは予定を表示するだけ。"""
    moves = plan_moves(folder)
    if not moves:
        print("整理するファイルはありませんでした。")
        return 0

    for src, dest in moves:
        if run:
            dest.parent.mkdir(exist_ok=True)
            dest = unique_destination(dest)
            src.rename(dest)
        print(f"{src.name}  →  {dest.parent.name}/{dest.name}")

    if run:
        print(f"\n{len(moves)} 個のファイルを整理しました。")
    else:
        print(f"\n{len(moves)} 個のファイルが上のように整理されます。")
        print("実際に動かすときは、最後に --run を付けて実行してください。")
    return len(moves)


def main():
    parser = argparse.ArgumentParser(description="ファイルを種類ごとのフォルダに振り分けます。")
    parser.add_argument("folder", help="整理したいフォルダの場所")
    parser.add_argument("--run", action="store_true", help="確認ではなく、実際にファイルを動かす")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser()
    if not folder.is_dir():
        print(f"フォルダが見つかりません: {folder}")
        sys.exit(1)

    organize(folder, run=args.run)


if __name__ == "__main__":
    main()
