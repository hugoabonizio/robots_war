class Chat:
	def __init__(self, conn):
		self.conn = conn
		self.buffer = ''
		self.conversation = []

	def write(self, char):
		self.buffer += chr(char)

	def backspace(self):
		self.buffer = self.buffer[:-1]

	def send(self):
		conn.send('chat:message=' + self.buffer + ';')
		self.add_message('You', self.buffer)
		self.buffer = ''

	def add_message(self, who, message):
		#if len(self.conversation) >= 5:
		#	self.conversation.__delitem__(0)
		self.conversation.append(who + ': ' + message)
