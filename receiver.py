import socket
import sys
import os
import time
import hashlib

class Receiver:
    
    PORT = 8000
    BUFFER_SIZE = 8192
    DESTINATION_DIR = "files"
    
    def __init__(self):
        if len(sys.argv) < 2:
            self.host = socket.gethostbyname(socket.gethostname())
        else:
            self.host = sys.argv[1]
        self.checksum = hashlib.md5()
        if not os.path.isdir(Receiver.DESTINATION_DIR):
            os.mkdir(Receiver.DESTINATION_DIR)
    
    def receive_file(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, Receiver.PORT))
            s.listen()
            print("Listening on", self.host, "on port", Receiver.PORT)
            print("Waiting for sender...")
            connection, addr = s.accept()
            with connection:
                start = time.time()
                print("Connected to", addr)
                filename = connection.recv(Receiver.BUFFER_SIZE).decode()
                filename = os.path.basename(os.path.abspath(filename))
                print("File being received:", filename)
                connection.sendall(b"<FILENAME>")
                file_size = int(connection.recv(Receiver.BUFFER_SIZE).decode())
                connection.sendall(b"<FILESIZE>")
                print("File Size:", file_size/1024/1024, "MB")
                size_left = file_size
                with open(f"{Receiver.DESTINATION_DIR}/{filename}", "wb") as file:
                    current_buffer_size = min(Receiver.BUFFER_SIZE, size_left)
                    while size_left > 0:
                        data = connection.recv(current_buffer_size)
                        file.write(data)
                        self.checksum.update(data)
                        size_left -= current_buffer_size
                        current_buffer_size = min(current_buffer_size, size_left)
                connection.sendall(b"<FILE>")
                print("Checking checksum")
                original_checksum = connection.recv(Receiver.BUFFER_SIZE).decode()
                if original_checksum != self.checksum.hexdigest():
                    print("File transfer not successful.")
                    os.remove(f"{Receiver.DESTINATION_DIR}/{filename}")
                else:
                    print("File received successfully!!")
                print("Time Taken:", time.time() - start)


if __name__ == "__main__":
    receiver = Receiver()
    receiver.receive_file()
