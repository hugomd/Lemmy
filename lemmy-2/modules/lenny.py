from module import Module
import random

class Lenny(Module):
	info = 'Posts Lennies'

	cmd_lenny_usage = [ 'lenny' ]
	async def cmd_lenny(self, message, args, kwargs):
		await self.client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')

	cmd_lennies_usage = [ 'lennies' ]
	async def cmd_lennies(self, message, args, kwargs):
		lennies = ["""░░░░░░░░░░░░▄▄▄▄░░░░░░░░░░░░░░░░░░░░░░░▄▄▄▄▄
░░░█░░░░▄▀█▀▀▄░░▀▀▀▄░░░░▐█░░░░░░░░░▄▀█▀▀▄░░░▀█▄
░░█░░░░▀░▐▌░░▐▌░░░░░▀░░░▐█░░░░░░░░▀░▐▌░░▐▌░░░░█▀
░▐▌░░░░░░░▀▄▄▀░░░░░░░░░░▐█▄▄░░░░░░░░░▀▄▄▀░░░░░▐▌
░█░░░░░░░░░░░░░░░░░░░░░░░░░▀█░░░░░░░░░░░░░░░░░░█
▐█░░░░░░░░░░░░░░░░░░░░░░░░░░█▌░░░░░░░░░░░░░░░░░█
▐█░░░░░░░░░░░░░░░░░░░░░░░░░░█▌░░░░░░░░░░░░░░░░░█
░█░░░░░░░░░░░░░░░░░░░░█▄░░░▄█░░░░░░░░░░░░░░░░░░█
░▐▌░░░░░░░░░░░░░░░░░░░░▀███▀░░░░░░░░░░░░░░░░░░▐▌
░░█░░░░░░░░░░░░░░░░░▀▄░░░░░░░░░░▄▀░░░░░░░░░░░░█
░░░█░░░░░░░░░░░░░░░░░░▀▄▄▄▄▄▄▄▀▀░░░░░░░░░░░░░█""", "ヽ( ͡° ͜ʖ ͡°)ﾉ", "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)", "( ͡o ͜ʖ ͡o)", "͡° ͜ʖ ͡ -", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "( ͡ ͡° ͡°  ʖ ͡° ͡°)", "(ง ͠° ͟ل͜ ͡°)ง", "( ͡° ͜ʖ ͡ °)", "(ʖ ͜° ͜ʖ)", "[ ͡° ͜ʖ ͡°]", "( ͡o ͜ʖ ͡o)", "{ ͡• ͜ʖ ͡•}", "( ͡° ͜V ͡°)", "( ͡^ ͜ʖ ͡^)", "( ‾ʖ̫‾)", "( ͡°╭͜ʖ╮͡° )", "ᕦ( ͡°╭͜ʖ╮͡° )ᕤ", "(σ ͟ʖσ)", "( ͡°ل͜ ͡°)", "(⚆ ͜ʖ⚆)", "( ͡°⍘ ͡°)", "(´• ͜ʖ •`)", "(Ȍ ͜ʖȌ)", "(❍⍘❍)", "( ͡°‿‿ ͡°)", "(☞ ͡° ͜ʖ ͡°)☞", "(づ ͡° ͜ʖ ͡°)づ", "(☞๏ ͜ʖ๏)☞", "(   ͡ °   ͜ ʖ   ͡ ° )", "(ಠ ͜ʖ ಠ)", "(    ͡   °    ͜   ʖ    ͡   °   )", "(╭☞ ͡° ͜ʖ ͡° )╭☞", "https://i.imgur.com/5qAb7gO.png"]
		await self.client.send_message(message.channel, random.choice(lennies))
