from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from generate_reply_completed import generateReply
from tag_data import create_tag_freq_table
from keyphrases import getPhrases
import json

# Simple WebSocket for single-user chat bot
class ChatServer(WebSocket):


    def handleMessage(self):
        # echo message back to client
        message = self.data
        param = create_tag_freq_table(getPhrases(message))
        self.sendMessage(json.dumps(param))
        response = generateReply(message)
        self.sendMessage(response)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


#print(generateReply("I am not cool."))
server = SimpleWebSocketServer('', 8080, ChatServer)
server.serveforever()
