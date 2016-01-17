import discord
import asyncio
import shlex
from PIL import Image
import random
import datetime
import re

class DecomposedMessage:
	def __init__(self, command, params, flags):
		self.command = command
		self.params = params
		self.flags = flags

def ParseMessage(messageText):
	decomposedArray = shlex.split(messageText)
	
	command = decomposedArray[0].lower() if len(decomposedArray) > 0 else None
	
	params = []
	i = 1
	while i < len(decomposedArray) and decomposedArray[i][0] != "-":
		params.append(decomposedArray[i])
		i += 1

	flags = []
	while i < len(decomposedArray):
		if decomposedArray[i][0] == "-" and not re.fullmatch("-\d+(.\d+)?", decomposedArray[i]):
			flags.append([decomposedArray[i].lower()])
		else:
			flags[-1].append(decomposedArray[i])
		i += 1

	return DecomposedMessage(command, params, flags)

async def SendEmote(client, msg):
	await client.send_message(msg.channel, "__**" + msg.author.name + "**__")
	await client.send_file(msg.channel, "pics/emotes/" + msg.content + ".png")
	await client.delete_message(msg)

async def SendSticker(client, msg):
	await client.send_message(msg.channel, "__**" + msg.author.name + "**__")
	await client.send_file(msg.channel, "pics/stickers/" + msg.content + ".png")
	await client.delete_message(msg)

def StripUnicode(string):
	stripped = [c for c in string if 0 < ord(c) < 127]
	return "".join(stripped)

def IsAdmin(member):
	return "administrator" in [role.name for role in member.roles]

def IsModOrAbove(member):
	return "administrator" in [role.name for role in member.roles] or "moderator" in [role.name for role in member.roles] or "robots" in [role.name for role in member.roles]

def IsRole(role, member):
	return role in [role.name for role in member.roles]

def FindUserByName(members, username):
	return discord.utils.find(lambda m: m.name == username, members)

def FindUserById(members, userId):
	return discord.utils.find(lambda m: m.id == userId, members)

def GetLemmyCoinBalance(res, user):
	cursor = res.sqlConnection.cursor()
	cursor.execute("SELECT LemmyCoinBalance FROM tblUser WHERE UserId = ?", (user.id,))
	record = cursor.fetchone()
	return (record[0] if record is not None else None)

def RemoveUnicode(string):
	return "".join([i if ord(i) < 128 else ' ' for i in string])

def TitleBox(string):
	return "\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n= " + string + " =\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n"

def CombineImages(images):
	width = 0
	for image in images:
		width += image.size[0]

	height = max([image.size[1] for image in images])

	result = Image.new("RGBA", (width, height))
	
	i = 0
	horizontalPointer = 0
	while i < len(images):
		result.paste(images[i], (horizontalPointer, 0))
		horizontalPointer += images[i].size[0]
		i += 1

	result.save("pics/result.png")

def LogEmoteUse(res, sender, emote):
	cursor = res.sqlConnection.cursor()
	newId = random.uniform(0.0, 1.0)
	cursor.execute("INSERT INTO tblEmoteUse (DateTime, UserId, Emote) VALUES (?, ?, ?)", (datetime.datetime.now(), sender.id, emote))
	res.sqlConnection.commit()

async def LogMessage(msg):
	metadata = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => " + ("(private channel)" if msg.channel.is_private else msg.channel.name) + ": "
	tab = "".join([" " for _ in range(len(metadata))])
	print(metadata + ("(Non-text message or file)" if not msg.content else RemoveUnicode(msg.content).replace("\n", "\n" + tab)))

async def LogMessageEdit(before, after):
	metadata = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + before.author.name + " /> " + ("(private channel)" if before.channel.is_private else before.channel.name) + ": "
	tab = "".join([" " for _ in range(len(metadata))])
	print(metadata + ("(Non-text message or file)" if not before.content else RemoveUnicode(before.content).replace("\n", "\n" + tab)))
	print(tab[:-3] + "└> ", end="")
	print("(Non-text message or file)" if not after.content else RemoveUnicode(after.content).replace("\n", "\n" + tab))

async def LogMessageDelete(msg):
	metadata = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " x> " + ("(private channel)" if msg.channel.is_private else msg.channel.name) + ": "
	tab = "".join([" " for _ in range(len(metadata))])
	print(metadata + ("(Non-text message or file)" if not msg.content else RemoveUnicode(msg.content).replace("\n", "\n" + tab)))

##################
# Archived Utils #
##################

# def GetNthFlag(n, params):
# 	for i in range(0, len(params)):
# 		if params[i][0] == "-":
# 			if n == 1:
# 				if i + 1 < len(params) and params[i + 1][0] != "-":
# 					return [params[i], params[i + 1]]
# 				else:
# 					return [params[i], None]
# 			else:
# 				n -= 1
# 	return None

# def GetNthFlagWith2Params(n, params):
# 	for i in range(0, len(params)):
# 		if params[i][0] == "-":
# 			if n == 1:
# 				if i + 1 < len(params) and params[i + 1][0] != "-":
# 					ret = [params[i], params[i + 1], None]
# 					if i + 2 < len(params) and params[i + 2][0] != "-":
# 						ret[2] = params[i + 2]
# 					return ret
# 				else:
# 					return [params[i], None, None]
# 			else:
# 				n -= 1
# 	return None

# def GetNthFlagWithAllParams(n, params):
# 	for i in range(0, len(params)):
# 		if params[i][0] == "-":
# 			if n == 1:
# 				ret = [params[i]]
# 				while i+1 < len(params) and params[i+1][0] != "-":
# 					ret.append(params[i+1])
# 					i += 1
# 				return ret
# 			else:
# 				n -= 1
# 	return None