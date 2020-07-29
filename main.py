from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
import logging as logger
from pyrogram import Client, Filters, Message
from pyrogram.api.functions.help import GetConfig
from pyrogram.errors import FloodWait
import re
import res
from res import Configurations

configurations_map = {
	"commands": "commands",
	"database": "database",
	"logger": "logger"
}

loop = asyncio.get_event_loop()

config = Configurations("config/config.json", configurations_map)
loop.run_until_complete(config.parse())
config.set("app_hash", os.environ.pop("app_hash", None))
config.set("app_id", int(os.environ.pop("app_id", 0)))
config.set("bot_token", os.environ.pop("bot_token", None))
config.set("bot_username", os.environ.pop("bot_username", None))

connection = pymysql.connect(
	host=config.get("database")["host"],
	user=os.environ.pop("database_username", config.get("database")["username"]),
	password=os.environ.pop("database_password", config.get("database")["password"]),
	database=config.get("bot_username"),
	port=config.get("database")["port"],
	charset="utf8",
	cursorclass=pymysql.cursors.DictCursor,
	autocommit=False)

logger.basicConfig(
	filename=config.get("logger")["path"],
	datefmt="%d/%m/%Y %H:%M:%S",
	format=config.get("logger")["format"],
	level=config.get("logger").pop("level", logger.INFO))

scheduler = AsyncIOScheduler()

with connection.cursor() as cursor:
	logger.info("Initializing the Admins ...")
	cursor.execute("SELECT `id` FROM `Admins` WHERE `username`=%(user)s;", {
		"user": "username"
	})
	config.set("creator", cursor.fetchone()["id"])

	logger.info("Admins initializated\nSetting the admins list ...")
	cursor.execute("SELECT `id` FROM `Admins`;")
	admins_list = list(map(lambda n: n["id"], cursor.fetchall()))

logger.info("Admins setted\nInitializing the Client ...")
app = Client(session_name=config.get("bot_username"), api_id=config.get("app_id"), api_hash=config.get("app_hash"), bot_token=config.get("bot_token"), lang_code="it", workdir=".", parse_mode="html")


@app.on_message(Filters.command("help", prefixes="/") & Filters.user(admins_list) & Filters.private)
async def help(_, message: Message):
	# /help
	global admins_list, config

	commands = config.get("commands")

	# Filter the commands list in base at their domain
	if message.from_user.id != config.get("creator"):
		commands = list(filter(lambda n: n["domain"] != "creator", commands))

	await res.split_reply_text(config, message, "In this section you will find the list of the command of the bot.\n\t{}".format("\n\t".join(list(map(lambda n: "<code>/{}{}</code> - {}".format(n["name"], " {}".format(n["parameters"]) if n["parameters"] != "" else n["parameters"], n["description"])), commands))), quote=False)

	logger.info("I\'ve answered to /help because of {}.".format("@{}".format(message.from_user.username) if message.from_user.username is not None else message.from_user.id))


@app.on_message(Filters.command("report", prefixes="/") & Filters.user(config.get("creator")) & Filters.private)
async def report(_, message: Message):
	# /report
	global config

	await res.split_reply_text(config, message, "\n".join(list(map(lambda n: "{} - {}".format(n["name"], n["description"]), config.get("commands")))), quote=False)

	logger.info("I\'ve answered to /report because of {}.".format("@{}".format(message.from_user.username) if message.from_user.username is not None else message.from_user.id))


@app.on_message(Filters.command("start", prefixes="/") & Filters.user(admins_list) & Filters.private)
async def start(client: Client, message: Message):
	# /start
	global config, connection, scheduler

	# Scheduling the functions
	scheduler.add_job(res.memo, CronTrigger(hour=8, minute=00, timezone="Europe/Rome"), kwargs={
		"client": client,
		"memo_type": "Phosphorus and Folic Acid",
		"config": config,
		"connection": connection
	})
	scheduler.add_job(res.memo, CronTrigger(hour=20, minute=0, timezone="Europe/Rome"), kwargs={
		"client": client,
		"memo_type": "Iron and vitamin B12",
		"config": config,
		"connection": connection
	})
	scheduler.add_job(res.memo, CronTrigger(day=15, hour=13, minute=0, timezone="Europe/Rome"), kwargs={
		"client": client,
		"memo_type": "vitamin D",
		"config": config,
		"connection": connection
	})

	# Setting the maximum message length
	max_length = await client.send(functions.help.GetConfig())
	config.set("message_max_length", max_length.message_length_max)

	# Retrieving the bot id
	bot = await client.get_users(config.get("bot_username"))
	config.set("bot_id", bot.id)

	await res.split_reply_text(config, "Welcome @{}.\nThis bot have the aim of reminding @violetbat to take supplements.".format(message.from_user.username), quote=False)
	logger.info("I\'ve answered to /start because of {}.".format("@{}".format(message.from_user.username) if message.from_user.username is not None else message.from_user.id))


@app.on_message(res.unknown_filter(config) & Filters.user(admins_list) & Filters.private)
async def unknown(_, message: Message):
	global config

	await res.split_reply_text(config, message, "This command isn\'t supported.", quote=False)
	logger.info("I managed an unsupported command.")


logger.info("Client initializated\nStarted serving ...")
scheduler.start()
app.run()
connection.close()
