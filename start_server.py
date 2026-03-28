#!/usr/bin/env python3
"""
観測者のいない記録 — ローカルプレビューサーバー
実行方法: python3 start_server.py
ブラウザで http://localhost:8080/game.html?new=1 を開く
"""
import http.server, webbrowser, os, threading

PORT = 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass  # ログ抑制

def open_browser():
    import time; time.sleep(0.8)
    webbrowser.open(f'http://localhost:{PORT}/game.html?new=1')

threading.Thread(target=open_browser, daemon=True).start()
print(f"サーバー起動中: http://localhost:{PORT}/game.html?new=1")
print("終了するには Ctrl+C を押してください")
http.server.HTTPServer(('', PORT), Handler).serve_forever()
