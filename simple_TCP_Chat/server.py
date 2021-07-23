import threading
import socket

host = '127.0.0.1' # localhost
port = 55554

# 소켓의 초기화 및 명시
#  1. 어떠 종류의 소켓을 원하는지?
#  2. 어떤 종류의 프로토콜을 사용할 것인지?
#  3. 어떤 IP를 사용 할 것인지?
#  4. 어떤 Port를 사용 할 것인지?

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #  1. 인터넷 소켓을 사용 2. TCP 사용
server.bind((host, port)) # 3. 명시한 local_IP 사용 , 4. 명시한 Port 사용 
server.listen() # 서버가 클라이언트의 접속을 허용

clients = [] # 클라이언트를 저장할 리스트
nicknames = [] # 클라이언트가 지정한 닉네임을 저장할 리스트

def broadcast(message): # 연결된 모든 클라이언트에 메세지를 송출하는 메소드
    for client in clients:
        client.send(message)

def handle(client): # 클라이언트를 매개변수로 받아들인다.
    while True: # 클라이언트가 서버에 연결될 때마다 반복
        try: # 클라이언트 메세지를 보낸다면 클라이언트로부터 메세지를 받고 연결된 모든 클라이언트에 송출한다.
            message = client.recv(1024)
            broadcast(message)
        except : # 예외 발생시 해당 클라이언트의 인덱스 값을 가져와 각각의 리스트에서 제거하고 연결을 차단하고 종료한다. 
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} is left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break

def receive(): # 서버 실행 후 연결을 시도하는 클라이언트들의 요청을 받는다.
    while True:
        client, address = server.accept() # 서버에 클라이언트가 연결되면 해당 클라이언트의 주소를 받아서 출력한다.
        print(f"connected with {str(address)}")

        client.send("NICK".encode('ascii')) # 클라이언트가 연결돠면 해당 문자열을 보내 닉네임이 요청되었음을 알린다.
        nickname = client.recv(1024).decode('ascii') # 후 해당 클라이언트와 클라이언트가 송출한 닉네임을 각각 리스트에 추가한다.
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        client.send("connected to the server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,)) # 병렬처리를 위한 스레드 사용
        thread.start()

print("server is listening...")
receive()
