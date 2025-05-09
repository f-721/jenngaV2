from http.server import BaseHTTPRequestHandler, HTTPServer

# 各デバイスの心拍数を保存する辞書
heart_rate_map = {}

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 心拍数表示（すべてのデバイス分）
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        if not heart_rate_map:
            self.wfile.write('心拍数データがない'.encode('utf-8'))
        else:
            response = ""
            for device_id, bpm in heart_rate_map.items():
                response += f"{device_id} : {bpm}\n"
            self.wfile.write(response.encode('utf-8'))

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
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'http://192.168.101.76:8081/index.html') #opt押しながらWi-FiでPCのIPアドレス表示
    httpd.serve_forever()

if __name__ == '__main__':
    run()