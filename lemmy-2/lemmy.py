import discord
import datetime
import asyncio
import os
import os.path
import json
import importlib
import sys

sys.path.append('modules')

class Lemmy:
	class NoConfigException(Exception):
		def __init__(self, message=None):
			if message is None:
				message = 'config.json does not exist (create it from config.example.json)'

			super(NoConfigException, self).__init__(message)


	def __init__(self, token):
		self.client = discord.Client()
		self.modules = {}

		# perform setup
		self.load_all()

		# register events
		@self.client.event
		async def on_message(message):
			context = message.channel.server.name if not type(message.channel) == discord.channel.PrivateChannel else None
			recipient = '#' + message.channel.name if not type(message.channel) == discord.channel.PrivateChannel else ', '.join([user.name for user in message.channel.recipients])

			context_phrase = f'({context}) ' if context else ''
			attachments_phrase = ' +' + '📎' * len(message.attachments) if len(message.attachments) > 0 else ''

			self.log(f'{context_phrase}{message.author.name} => {recipient}{attachments_phrase}: {message.content}')

			# pass the event to the modules
			for _, module in self.modules.items():
				await module.on_message(message)

		@self.client.event
		async def on_ready():
			self.log('Logged in.')

		# log in
		self.log('Logging in...')
		# wrap this in a try block to gracefully shut down the bot when a KeyboardInterrupt is sent
		try:
			self.client.run(token)
		except KeyboardInterrupt:
			pass

		# at this point the bot has shut down
		self.log('Shut down.')


	def log(self, message):
		output = '[{}] {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)

		print(output)

		if self.config['log_file']:
			with open(self.config['log_file'], 'a', encoding='utf8') as f:
				f.write(output + '\n')


	def load_all(self):
		self.load_config()
		self.load_modules()


	def load_config(self):
		if not os.path.isfile('config.json'):
			raise NoConfigException

		self.config = json.load(open('config.json', 'r'))


	def load_modules(self):
		manifest = json.load(open('modules/manifest.json', 'r'))

		for module_name, class_name in manifest.items():
			module = importlib.import_module(module_name)
			importlib.reload(module)   # changes to the module will be loaded (for if this was called again while the bot is running)
			class_ = getattr(module, class_name)
			self.modules[class_name] = class_(self)


	def config_try_key(self, *path):
		node = self.config
		for step in path:
			if type(node) == dict and step in node:
				node = node[step]
			else:
				raise KeyError(step)

		return node


	def resolve_symbol(self, channel):
		try:
			symbol = self.config_try_key("server_config", channel.server.id, "symbol")
		except ( AttributeError, KeyError ):
			symbol = self.config["default_symbol"]
		return symbol



if __name__ == '__main__':
	if not os.path.isfile('config.json'):
		raise NoConfigException

	lemmy = Lemmy(json.load(open('config.json', 'r'))['token'])
