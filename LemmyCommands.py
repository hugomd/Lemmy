# Lemmy's stuff
import LemmyUtils as Lutils
import RandomLenny

# Other stuff
import random
import discord
import os
from os import listdir
from os.path import isfile, join
import json
import sqlite3
import datetime

def help(client, res, msg, params):
	client.send_message(msg.channel, "http://lynq.me/lemmy")

def emotes(client, res, msg, params):
	client.send_message(msg.channel, "http://lynq.me/lemmy/#emotes")

def stickers(client, res, msg, params):
	client.send_message(msg.channel, "http://lynq.me/lemmy/#stickers")

def lenny(client, res, msg, params):
	flag = Lutils.GetNthFlag(1, params)
	if flag == None:
		client.send_message(msg.channel, res.lennies[random.randint(0, len(res.lennies)-1)])
	elif flag == "-og":
		client.send_message(msg.channel, res.lenny)
	elif flag == "-r":
		client.send_message(msg.channel, RandomLenny.randomLenny())
	#client.send_message(msg.channel, "This was sent without closing the script.")

def logout(client, res, msg, params):
	print("User with id " + str(msg.author.id) + " attempting to logout.")
	if Lutils.IsAdmin(msg.author):
		client.send_message(msg.channel, "Shutting down.")
		client.logout()

def restart(client, res, msg, params):
	print("User with id " + str(msg.author.id) + " attempting to restart.")
	if Lutils.IsAdmin(msg.author):
		client.send_message(msg.channel, "Restarting.")
		client.logout()

def refresh(client, res, msg, params):
	refreshedEmotes = [ os.path.splitext(f)[0] for f in listdir("pics/emotes") if isfile(join("pics/emotes",f)) ]
	refreshedStickers = [ os.path.splitext(f)[0] for f in listdir("pics/stickers") if isfile(join("pics/stickers",f)) ]

	newEmotes = [item for item in refreshedEmotes if item not in res.emotes]
	newStickers = [item for item in refreshedStickers if item not in res.stickers]

	res.emotes = refreshedEmotes
	res.stickers = refreshedStickers

	if len(newEmotes) > 0:
		client.send_message(msg.channel, "__**New emotes:**__")

		for emote in newEmotes:
			client.send_message(msg.channel, emote)
			client.send_file(msg.channel, "pics/emotes/" + emote + ".png")

	if len(newStickers) > 0:
		client.send_message(msg.channel, "__**New stickers:**__")

		for sticker in newStickers:
			client.send_message(msg.channel, sticker)
			client.send_file(msg.channel, "pics/stickers/" + sticker + ".png")

	client.delete_message(msg)

def correct(client, res, msg, params):
	client.send_message(msg.channel, "https://youtu.be/OoZN3CAVczs")

def eightball(client, res, msg, params):
	responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
	client.send_message(msg.channel, msg.author.mention() + " :8ball: " + responses[random.randint(0, len(responses)-1)])

def userinfo(client, res, msg, params):
	if len(params) > 0:
		username = params[0]
		user = Lutils.FindUserByName(msg.channel.server.members, username)
		if user:
			message = "**Username:** " + user.name + "\n**ID:** " + user.id

			balance = Lutils.GetLemmyCoinBalance(res, user)
			if balance is not None:
				message += "\n**LemmyCoin Balance:** L$" + str(balance)

			message += "\n**Avatar URL:** " + user.avatar_url()

			client.send_message(msg.channel, message)
		else:
			client.send_message(msg.channel, "User not found.")

def channelinfo(client, res, msg, params):
	if len(params) > 0:
		channelName = params[0]
		channel = discord.utils.find(lambda m: m.name == channelName, [x for x in msg.channel.server.channels if x.type == "text"])
		if channel:
			client.send_message(msg.channel, "**Channel name: **" + channel.mention() + "\n**ID: **" + channel.id)
		else:
			client.send_message(msg.channel, "Channel not found.")

def james(client, res, msg, params):
	if len(params) > 0:
		flagPair = Lutils.GetNthFlag(1, params)
		
		if flagPair:
			update = False
			flag = flagPair[0]
			gameTag = flagPair[1]

			if flag == "-tags":
				response = "```"
				for key in res.jamesDb:
					response += "\n" + key + " (" + res.jamesConverter[key] + ")"
					for userId in res.jamesDb[key]:
						user = Lutils.FindUserById(msg.channel.server.members, userId)
						response += "\n> " + user.name
					response += "\n"
				response += "```"
				client.send_message(msg.channel, response)

			elif flag == "-join":
				if not gameTag:
					client.send_message(msg.channel, msg.author.mention() + " was not added to any tag: No tag was specified.")
				else:
					if gameTag in res.jamesDb:
						if msg.author.id in res.jamesDb[gameTag]:
							client.send_message(msg.channel, msg.author.mention() + " was not added to '" + gameTag + "': User is already in '" + gameTag + "'.")
						else:
							update = True
							res.jamesDb[gameTag].append(msg.author.id)
							client.send_message(msg.channel, msg.author.mention() + " was successfully added to '" + gameTag + "'.")
					else:
						client.send_message(msg.channel, msg.author.mention() + " was not added to '" + gameTag + "': No such tag exists.")

			elif flag == "-leave":
				if not gameTag:
					client.send_message(msg.channel, msg.author.mention() + " was not removed from any tag: No tag was specified.")
				else:
					if gameTag in res.jamesDb:
						if msg.author.id in res.jamesDb[gameTag]:
							update = True
							res.jamesDb[gameTag] = [x for x in res.jamesDb[gameTag] if x != msg.author.id]
							client.send_message(msg.channel, msg.author.mention() + " was successfully removed from '" + gameTag + "'.")
						else:
							client.send_message(msg.channel, msg.author.mention() + " was not removed from '" + gameTag + "': User is not in '" + gameTag + "'.")
					else:
						client.send_message(msg.channel, msg.author.mention() + " was not removed from '" + gameTag + "': No such tag exists.")

			elif flag == "-create":
				if not Lutils.IsModOrAbove(msg.author):
					client.send_message(msg.channel, "No new tag created: User is not moderator or above.")
				else:
					if not gameTag:
						client.send_message(msg.channel, "No new tag created: No tag name was specified.")
					else:
						flagRecalc = Lutils.GetNthFlagWithAllParams(1, params)
						flag = flagRecalc[0]
						dataString = " ".join(flagRecalc[1:])
						split = dataString.split("#")
						if len(split) < 2:
							client.send_message(msg.channel, "New tag '" + split[0] + "' not created: No hash-separated display name was given.")
						else:
							tagName = split[0]
							displayName = split[1]

							if tagName in res.jamesDb:
								client.send_message(msg.channel, "New tag '" + tagName + "' not created: Tag already exists.")
							else:
								update = True
								res.jamesDb[tagName] = []
								res.jamesConverter[tagName] = displayName
								client.send_message(msg.channel, "New tag '" + tagName + "' successfully created with display name '" + displayName + "'.")

			elif flag == "-delete":
				if not Lutils.IsModOrAbove(msg.author):
					client.send_message(msg.channel, "No tag deleted: User is not moderator or above.")
				else:
					if not gameTag:
						client.send_message(msg.channel, "No tag deleted: No tag name was specified.")
					else:
						if gameTag in res.jamesDb:
							update = True
							res.jamesDb.pop(gameTag, None)
							res.jamesConverter.pop(gameTag, None)
							client.send_message(msg.channel, "Tag '" + gameTag + "' successfully deleted.")
						else:
							client.send_message(msg.channel, "Tag '" + gameTag + "' not deleted: Tag does not exist.")
							


			if update:
				try:
					with open("db/jamesDb.json", "w") as f:
						json.dump(res.jamesDb, f)
				except Exception as e:
					print("ERROR updating JamesDb! (" + str(e) + ")")
				else:
					print("JamesDb updated with " + str(len(res.jamesDb)) + " games.")

				try:
					with open("db/jamesConverter.json", "w") as f:
						json.dump(res.jamesConverter, f)
				except Exception as e:
					print("ERROR updating JamesConverter! (" + str(e) + ")")
				else:
					print("JamesConverter updated with " + str(len(res.jamesConverter)) + " games.")

		# No flags in message
		else:
			if len(params) > 0:
				print("Params, no flags")
				if params[0] in res.jamesDb:
					response = "Pinging "
					for userId in res.jamesDb[params[0]]:
						user = Lutils.FindUserById(msg.channel.server.members, userId)
						if user is not None:
							response += user.mention() + " "
					response += "for " + res.jamesConverter[params[0]]
					client.send_message(msg.channel, response)

def happening(client, res, msg, params):
	client.send_message(msg.channel, "https://i.imgur.com/bYGOUHP.png")

def ruseman(client, res, msg, params):
	client.send_file(msg.channel, "pics/ruseman/" + random.choice(os.listdir("pics/ruseman/")))

def register(client, res, msg, params):
	if Lutils.IsAdmin(msg.author):
		if len(params) > 0:
			userId = params[0]
			
			cursor = res.sqlConnection.cursor()
			cursor.execute("SELECT COUNT(*) FROM tblUser WHERE UserId = ?", (userId,))
			if cursor.fetchone()[0] > 0:
				client.send_message(msg.channel, "User with id " + userId + " not registered to database: User already exists in database.")
			else:
				user = Lutils.FindUserById(msg.channel.server.members, userId)
				if not user:
					client.send_message(msg.channel, "User with id " + userId + " not registered to database: ID does not reference a Discord user on this server.")
				else:
					cursor.execute("INSERT INTO tblUser (UserId, LemmyCoinBalance) VALUES (?, 0)", (userId,))
					res.sqlConnection.commit()
					client.send_message(msg.channel, "User with id " + userId + " (" + user.mention() + ") successfully registered to database.")

def lemmycoin(client, res, msg, params):
	flagpair = Lutils.GetNthFlagWith2Params(1, params)

	if flagpair:
		flag = flagpair[0]
		param1 = flagpair[1]
		param2 = flagpair[2]

		if flag == "-balance":
			user = None

			if param1 is None:
				user = msg.author
			else:
				targetUser = Lutils.FindUserByName(msg.channel.server.members, param1)
				if targetUser is None:
					client.send_message(msg.channel, "User '" + param1 + "' was not found on this Discord server.")
				else:
					user = targetUser

			if user is not None:
				balance = Lutils.GetLemmyCoinBalance(res, user)

				if balance is None:
					client.send_message(msg.channel, user.mention() + " does not have a LemmyCoin balance because they have not been registered in the database.")
				else:
					client.send_message(msg.channel, user.mention() + " has a LemmyCoin balance of L$" + str(balance) + ".")

		elif flag == "-pay":
			if param1 is not None:
				target = Lutils.FindUserByName(msg.channel.server.members, param1)
				if target is None:
					client.send_message(msg.channel, "LemmyCoins not sent: User '" + param1 + "' was not found on this server.")
				elif param2 is None:
					client.send_message(msg.channel, "No LemmyCoins paid to " + target.name + ": No amount was specified.")
				else:
					try:
						amount = float(param2)
					except ValueError:
						client.send_message(msg.channel, "No LemmyCoins paid to " + target.name + ": Amount was incorrectly formatted.")
					else:
						if amount <= 0:
							client.send_message(msg.channel, "No LemmyCoins paid to " + target.name + ": Amount must be greater than zero.")
						else:
							cursor = res.sqlConnection.cursor()
							cursor.execute("SELECT COUNT(*) FROM tblUser WHERE UserId = ?", (target.id,))
							result = cursor.fetchone()[0]

							if result == 0:
								client.send_message(msg.channel, "No LemmyCoins paid to " + target.name + ": " + target.name + " has not been registered in the database.")
							else:
								cursor.execute("SELECT LemmyCoinBalance FROM tblUser WHERE UserId = ?", (msg.author.id,))
								senderBalance = cursor.fetchone()[0]

								if senderBalance < amount:
									client.send_message(msg.channel, "No LemmyCoins paid to " + target.name + ": " + msg.author.mention() + " does not have enough LemmyCoins in their account to make the payment.")
								else:
									cursor.execute("UPDATE tblUser SET LemmyCoinBalance = LemmyCoinBalance - ? WHERE UserId = ?", (amount, msg.author.id))
									cursor.execute("UPDATE tblUser SET LemmyCoinBalance = LemmyCoinBalance + ? WHERE UserId = ?", (amount, target.id))
									cursor.execute("INSERT INTO tblLemmyCoinPayment (DateTime, SenderId, ReceiverId, Amount) VALUES (?, ?, ?, ?)", (datetime.datetime.now(), msg.author.id, target.id, amount))
									res.sqlConnection.commit()
									client.send_message(msg.channel, "**L$" + str(amount) + "** successfully sent to " + target.mention() + " by " + msg.author.mention() + ".")