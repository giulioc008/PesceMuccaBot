import asyncio
import datetime
from pymysql.connections import Connection
from pyrogram import Client, Filters, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait
import re
from res.configurations import Configurations


async def memo(client: Client, memo_type: str, config: Configurations, connection: Connection):
	if memo_type == "vitamin D" and datetime.date.today().day != 15:
		return

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM `Admins`;")
		for i in cursor.fetchall():
			if i["id"] == config.get("creator"):
				await client.send_message(i["id"], "Hi {};\nYou\'re testing the bot.".format(i["first_name"] if i["first_name"] is not None else "@{}".format(i["username"])))
			else:
				await client.send_message(i["id"], "Hi {};\nI wanted to remind you that you have to take {}.".format(i["first_name"] if i["first_name"] is not None else "@{}".format(i["username"]), memo_type))

	logger.info("I have remind the supplements.")


async def split_edit_text(config: Configurations, message: Message, text: str, **options):
	"""
		A coroutine that edits the text of a message; if text is too long sends more messages.
		:param message: Message to edit
		:param text: Text to insert
		:return: None
	"""
	await message.edit_text(text[: config.get("message_max_length")], options)
	if len(text) >= config.get("message_max_length"):
		for i in range(1, len(text), config.get("message_max_length")):
			try:
				await message.reply_text(text[i : i + config.get("message_max_length")], options, quote=True)
			except FloodWait as e:
				await asyncio.sleep(e.x)


async def split_reply_text(config: Configurations, message: Message, text: str, **options):
	"""
		A coroutine that reply to a message; if text is too long sends more messages.
		:param message: Message to reply
		:param text: Text to insert
		:return: None
	"""
	await message.reply_text(text[: config.get("message_max_length")], options)
	if len(text) >= config.get("message_max_length"):
		for i in range(1, len(text), config.get("message_max_length")):
			try:
				await message.reply_text(text[i : i + config.get("message_max_length")], options)
			except FloodWait as e:
				await asyncio.sleep(e.x)


def unknown_filter(config: Configurations):
	def func(flt, message: Message):
		text = message.text
		if text:
			message.matches = list(flt.p.finditer(text)) or None
			if message.matches is False and text.startswith("/") is True and len(text) > 1:
				return True
		return False

	commands = list(map(lambda n: n["name"], config.get("commands")))

	return Filters.create(func, "UnknownFilter", p=re.compile("/{}".format("|/".join(commands)), 0))
