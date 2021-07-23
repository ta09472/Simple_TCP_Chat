import socket
import threading

# 클라이언트는 닉네임을 입력하고 서버에 연결한다.
nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 서버와 동일한 소켓과 프로토콜 선언
client.connect(('127.0.0.1', 55554)) # 서버와 동일한 IP와 PORT에 접속

# 클라이언트의 첫번쩨 스레드
def receive(): # 서버로부터 데이터를 받는다.
    while True:
        try: # 메세지를 수신하고 출력한다.
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except: # 예외 발생시 연결을 차단한다. 
            print("An error occurred!")
            client.close()
            break
            
# 클라이언트의 두번째 스레드
def write(): # 서버에 메세지를 보낸다.
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# 송수신을 병렬적으로 처리
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
