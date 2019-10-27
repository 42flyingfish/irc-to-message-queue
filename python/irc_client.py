import socket
import pika

class irc:

    def __init__(self, HOST, PORT, NICK, PASS, CHAN):
        self.irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        self.NICK = NICK
        self.PASS = PASS
        self.CHANNEL_NAME = CHAN

    def joinChannel(self):
        self.irc_sock.connect((self.HOST, self.PORT))
        self.irc_sock.send(bytes(f'PASS {self.PASS}\n\r', 'utf-8'))
        self.irc_sock.send(bytes(f'NICK {self.NICK}\n\r', 'utf-8'))
        self.irc_sock.send(bytes(f'JOIN #{self.CHANNEL_NAME} \n\r', 'utf-8'))

    def listenAndSend(self):
        while True:
            messages = self.irc_sock.recv(1024).decode('utf-8')
            temp = messages.split('\n')
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
            channel = connection.channel()
            channel.queue_declare(queue='task_queue', durable=True)
            for message in temp:
                channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))
            connection.close()


