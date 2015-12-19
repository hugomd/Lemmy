import sys
sys.path.append('modules')

# Lemmy's stuff
import LemmyUtils as Lutils
import LemmyCommands as Lcmds
import LemmyResources as Lres
from FloodProtector import FloodProtector
from CallLogger import CallLogger

# Other stuff
import discord
import datetime
import codecs

class LemmyBot:
	def __init__(self, username, password):
		self.res = Lres.LemmyResources()
		self.res.Load()

		# Map of function names to their equivalent function pointers
		self.funcMap = {
			"help": Lcmds.help,
			"emotes": Lcmds.emotes,
			"stickers": Lcmds.stickers,
			"lenny": Lcmds.lenny,
			"refresh": Lcmds.refresh,
			"f5": Lcmds.refresh,
			"correct": Lcmds.correct,
			"8ball": Lcmds.eightball,
			"userinfo": Lcmds.userinfo,
			"channelinfo": Lcmds.channelinfo,
			"james": Lcmds.james,
			"happening": Lcmds.happening,
			"ruseman": Lcmds.ruseman,
			"register": Lcmds.register,
			"lemmycoin": Lcmds.lemmycoin,
			"nicememe": Lcmds.nicememe,
			"channelids": Lcmds.channelids,
			"serverid": Lcmds.serverid,
			"logout": Lcmds.logout
			#"restart": Lcmds.restart
		}

		self.floodProtectors = {
			"emote": FloodProtector(5),
			"sticker": FloodProtector(5)
		}

		self.callLogger = None

		self.client = discord.Client()
		print(Lutils.TitleBox("Logging Into Discord"))
		
		print("Attempting to log in.")
		try:
			self.client.login(username, password)
		except:
			print("ERROR logging into Discord!")
			input("Press any key to exit.\n")
			quit()

		@self.client.event
		def on_ready():
			print("Successfully logged in.")
			print("USERNAME: " + username)
			print("PASSWORD: " + "".join(["*" for x in password]))

			print(Lutils.TitleBox("Checking Channel Mapping"))

			warnings = False
			for server in self.client.servers:

				# Server hasn't been mapped at all
				if server.id not in self.res.voiceToTextChannelMaps and server.id not in self.res.textToVoiceChannelMaps:
					print("Warning! Server " + server.name + " does not have its voice or text channels mapped.")
					warnings = True

				# Server has had text channels mapped, but not voice channels
				elif server.id not in self.res.voiceToTextChannelMaps:
					print("Warning! Server " + server.name + " does not have its voice channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == "text" and channel.id not in self.res.textToVoiceChannelMaps[server.id]:
							print("  Warning! Server " + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")

				# Server has had voice channels mapped, but not text channels
				elif server.id not in self.res.textToVoiceChannelMaps:
					print("Warning! Server " + server.name + " does not have its text channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == "voice" and channel.id not in self.res.voiceToTextChannelMaps[server.id]:
							print("  Warning! Server " + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")

				# Server has had voice and text channels mapped
				else:
					print("Server " + server.name + " has its voice and text channels mapped.")
					for channel in server.channels:
						if channel.type == "text" and channel.id not in self.res.textToVoiceChannelMaps[server.id]:
							print("Warning! Server " + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")
							warnings = True
					for channel in server.channels:
						if channel.type == "voice" and channel.id not in self.res.voiceToTextChannelMaps[server.id]:
							print("Warning! Server " + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")
							warnings = True

			if not warnings:
				print("All channels of all servers have been mapped.")
				

			print(Lutils.TitleBox("Listening For Messages"))

			channelList = []
			for server in self.client.servers:
				for channel in server.channels:
					if channel.type == "voice":
						channelList.append(channel)
			self.callLogger = CallLogger(channelList)

		@self.client.event
		def on_message(msg):
			if msg.content:
				if msg.channel.is_private:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => (private channel): " + Lutils.RemoveUnicode(msg.content))
				else:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => " + msg.channel.name + ": " + Lutils.RemoveUnicode(msg.content))

				if msg.content[0] == "!":
					dmsg = Lutils.ParseMessage(msg.content)

					if dmsg.command.lower() in self.funcMap:
						self.funcMap[dmsg.command.lower()](self.client, self.res, msg, dmsg.params)

				elif msg.content in self.res.emotes and msg.author != self.client.user:
					if self.floodProtectors["emote"].Ready(msg.author.id):
						Lutils.SendEmote(self.client, msg)
						self.floodProtectors["emote"].Sent(msg.author.id)
					else:
						self.client.delete_message(msg)

				elif msg.content in self.res.stickers and msg.author != self.client.user:
					if self.floodProtectors["sticker"].Ready(msg.author.id):
						Lutils.SendSticker(self.client, msg)
						self.floodProtectors["sticker"].Sent(msg.author.id)
					else:
						self.client.delete_message(msg)

			else:
				if msg.channel.is_private:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => (private channel): (Non-text message or file)")
				else:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => " + msg.channel.name + ": (Non-text message or file)")

		@self.client.event
		def on_voice_state_update(member):
			channelList = []
			for server in self.client.servers:
				for channel in server.channels:
					if channel.type == "voice":
						channelList.append(channel)
			responses = self.callLogger.UpdateStatuses(channelList)

			for response in responses:
				channel = response[0]
				timeString = response[1]

				if channel.server.id in self.res.voiceToTextChannelMaps:
					textChannelId = self.res.voiceToTextChannelMaps[channel.server.id][channel.id]
					if textChannelId is not None:
						textChannel = discord.utils.find(lambda m: m.id == textChannelId, channel.server.channels)
						self.client.send_message(textChannel if textChannel is not None else channel.server.get_default_channel(), "Call ended in " + Lutils.StripUnicode(channel.name).strip() + ", duration " + timeString)

	def Start(self):
		self.client.run()