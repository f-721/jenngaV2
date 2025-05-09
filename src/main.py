from http.server import BaseHTTPRequestHandler, HTTPServer
import os
# 各デバイスの心拍数を保存する辞書
heart_rate_map = {}

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open("index.html", "r", encoding="utf-8") as f:
                    # content = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')  # Content-Typeを明示
                    self.send_header('Access-Control-Allow-Origin', '*') 
                    self.end_headers()

                    if heart_rate_map:
                        response = ""
                        for device_id, bpm in heart_rate_map.items():
                            response += f"{device_id} : {bpm}\n"
                        self.wfile.write(response.encode('utf-8'))
                        print("チンチンが"+response+"になった！")  # ←開発用ならOKだけど、本番コードには注意にゃ！
                    else:
                        self.wfile.write('心拍数データがない'.encode('utf-8'))

            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write('index.html が見つかりません'.encode('utf-8'))
        else:
            # 他のパスの場合は404エラーを返す
            self.send_response(404)
            self.end_headers()
            self.wfile.write('リクエストされたリソースが見つかりません'.encode('utf-8'))

            if not heart_rate_map:
                self.wfile.write('心拍数データがない'.encode('utf-8'))
            else:
                response = ""
                for device_id, bpm in heart_rate_map.items():
                    response += f"{device_id} : {bpm}\n"
                self.wfile.write(response.encode('utf-8'))
                print("うおおおおおおおおおおおおおおお")

    def do_POST(self):  
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        print(f"[POST受信] 内容: {post_data}")

        try:
            device_id, bpm = post_data.strip().split(":")
            heart_rate_map[device_id] = int(float(bpm))
            print(f"[更新] {device_id} → {bpm} bpm")

            self.send_response(200)
            self.end_headers()
            self.wfile.write('心拍数を受信しました'.encode('utf-8'))
        except Exception as e:
            print("エラー:", e)
            self.send_response(400)
            self.end_headers()
            self.wfile.write('無効なデータ形式です（例: device01:85）'.encode('utf-8'))

def run(port=8081):
    # スクリプトのディレクトリをカレントディレクトリに設定
    os.chdir(os.path.dirname(__file__))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler) 
    print(f'file:///Users/k21146kk/jenngaV2/src/index.html') #opt押しながらWi-FiでPCのIPアドレス表示
    httpd.serve_forever()

if __name__ == '__main__':
    run()
