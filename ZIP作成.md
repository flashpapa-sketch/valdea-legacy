# ヴァルデアの遺産 ZIP作成スキル

## 概要
game.html・guide.html・index.html・ogp.png・README.mdを一つのZIPにまとめてダウンロード可能にする。

## 実行前チェック
1. 全ファイルが /mnt/user-data/outputs/ に存在するか確認
2. 日付を自動取得してファイル名に使用（valdea-legacy-YYYYMMDD.zip）

## 手順
```python
import zipfile, os
from datetime import datetime

zip_path = f"/mnt/user-data/outputs/valdea-legacy-{datetime.now().strftime('%Y%m%d')}.zip"
files = [
    ("/mnt/user-data/outputs/index.html", "index.html"),
    ("/mnt/user-data/outputs/game.html", "game.html"),
    ("/mnt/user-data/outputs/guide.html", "guide.html"),
    ("/mnt/user-data/outputs/ogp.png", "ogp.png"),
    ("/mnt/user-data/outputs/README.md", "README.md"),
]
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for src, arcname in files:
        zf.write(src, arcname)
        print(f"  {arcname}: {os.path.getsize(src):,} bytes")
print(f"ZIP: {os.path.getsize(zip_path):,} bytes")
```

## 完了後
- present_filesでZIPをユーザーに渡す
- ZIPを作る前に必ずユーザーに確認を取ること
