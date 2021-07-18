import socket
import threading
import asyncio
import traceback
class Receiver():
    def __init__(self, newUpdateCallback):
        self.newUpdateCallback = newUpdateCallback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('127.0.0.1',9722))

        # 응답을 수신하는 쓰레드를 시작합니다.
        self.receive_thread = threading.Thread(target=self.receive_process)
        self.receive_thread.daemon = True
        self.receive_thread.start()
    def receive_process(self):
        while True:
            if self.socket is not None:
                try:
                    response, ip = self.socket.recvfrom(1024) # 응답을 받습니다.
                    response = response.decode('utf-8') # 디코딩하여 문자열로 만듭니다.
                    print(f'response : {response}')
                    asyncio.run(self.newUpdateCallback(response))
                except Exception as exc:
                    traceback.print_exc()
                    print("catch error")
