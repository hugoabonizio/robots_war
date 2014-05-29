class Chat:
	def __init__(self, conn):
		self.conn = conn
		self.buffer = ''
		self.conversation = []

	def write(self, char):
		if len(self.buffer) < 32: self.buffer += chr(char)

	def backspace(self):
		self.buffer = self.buffer[:-1]

	def send(self):
		self.conn.send('chat:message=' + self.buffer + ';')
		self.add_message('Me', self.buffer)
		self.buffer = ''

	def add_message(self, who, message):
		if who != 'Me': who = 'Enemy'
		if len(self.conversation) >= 5:
			self.conversation.__delitem__(0)
		self.conversation.append(who + ': ' + message)
