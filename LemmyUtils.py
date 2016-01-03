import discord
import asyncio
import shlex

class DecomposedMessage:
	def __init__(self, command, params):
		self.command = command
		self.params = params

def ParseMessage(message):
	# if message[0] == "!":
	# 	message = message[1:]
	decompArray = shlex.split(message)
	decomp = DecomposedMessage(decompArray[0], decompArray[1:])

	return decomp

def GetNthFlag(n, params):
	for i in range(0, len(params)):
		if params[i][0] == "-":
			if n == 1:
				if i + 1 < len(params) and params[i + 1][0] != "-":
					return [params[i], params[i + 1]]
				else:
					return [params[i], None]
			else:
				n -= 1
	return None

def GetNthFlagWith2Params(n, params):
	for i in range(0, len(params)):
		if params[i][0] == "-":
			if n == 1:
				if i + 1 < len(params) and params[i + 1][0] != "-":
					ret = [params[i], params[i + 1], None]
					if i + 2 < len(params) and params[i + 2][0] != "-":
						ret[2] = params[i + 2]
					return ret
				else:
					return [params[i], None, None]
			else:
				n -= 1
	return None

def GetNthFlagWithAllParams(n, params):
	for i in range(0, len(params)):
		if params[i][0] == "-":
			if n == 1:
				ret = [params[i]]
				while i+1 < len(params) and params[i+1][0] != "-":
					ret.append(params[i+1])
					i += 1
				return ret
			else:
				n -= 1
	return None

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