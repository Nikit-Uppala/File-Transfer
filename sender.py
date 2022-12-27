import socket
import sys
import os
import hashlib


class Sender:

    BUFFER_SIZE = 8192

    def __init__(self):
        self.checksum = hashlib.md5()
    
    def receive_ack(self, s):
        while True:
            ack = s.recv(Sender.BUFFER_SIZE)
            if not ack:
                continue
            break

    def send_file(self, addr, port, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((addr, port))
            print("Connected to", addr, "on port", port)
            with open(filename, "rb") as file:
                s.sendall(filename.encode("utf-8"))
                self.receive_ack(s)
                total_size = os.path.getsize(filename)
                size_left = total_size
                current_buffer_size = min(Sender.BUFFER_SIZE, size_left)
                s.sendall(str(total_size).encode("utf-8"))
                self.receive_ack(s)
                while size_left > 0:
                    data = file.read(current_buffer_size)
                    s.sendall(data)
                    self.checksum.update(data)
                    size_left -= current_buffer_size
                    current_buffer_size = min(size_left, current_buffer_size)
                print("File sent to the receiver")
            self.receive_ack(s)
            s.sendall(self.checksum.hexdigest().encode("utf-8"))
        print("Disconnected")



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Less arguments")
        quit()
    addr = sys.argv[1]
    port = int(sys.argv[2])
    filename = " ".join(sys.argv[3:])
    sender = Sender()
    sender.send_file(addr, port, filename)
