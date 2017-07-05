# -*- coding: utf-8 -*-
import importlib, config, telebot, jsonData, re, sys
from datetime import datetime
from telebot import types
from telebot import util

reload(sys)  
sys.setdefaultencoding('utf8')

bot = telebot.TeleBot(config.TOKEN)
working_plugins = []

# Define color codes
class textcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAILYELLOW = '\033[93m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\x1b[0m'
def is_banned(uid):
	banList = jsonData.load_data("data/banList.json")
	return str(uid) in banList
for i in config.ENABLED_PLUGINS:
	try:
		#importlib.import_module("plugins.{}".format(i))
		execfile("plugins/{}.py".format(i))
		print "{}Plugin {} loaded.{}".format(textcolor.OKGREEN, i, textcolor.RESET)
		working_plugins.append(i)
	except Exception as e:
		print "{}Failed to load plugin {}{}{}:{}\n{}{}{}".format(textcolor.FAILYELLOW, textcolor.RESET, textcolor.BOLD, i, textcolor.RESET, textcolor.FAIL, e, textcolor.RESET)
		
@bot.message_handler(func=lambda message: True)
def process_messages(msg):
	if msg.chat.type == "private":
		print """#Message\n[{}]
[{}] -> \"{}\"""".format(datetime.now().strftime("%Y/%m/%d - %H:%M"), msg.from_user.first_name.encode("utf-8"), msg.text.encode("utf-8"))

		if is_banned(msg.from_user.id):
			return
	if msg.chat.type != "private":
		print """#Message\n[{}]
[{}] - [{}] -> \"{}\"
""".format(datetime.now().strftime("%Y/%m/%d - %H:%M"), msg.from_user.first_name.encode("utf-8"), msg.chat.title.encode("utf-8"), msg.text.encode("utf-8"))
	patterns = []
	for v in working_plugins:
		try:
			exec("patterns = plugin_{}.patterns".format(v))
		except:
			pass
		
		for i in patterns:
			#matches = re.match(i, msg.text)
			exec("matches = re.match(r'{}', msg.text)".format(i))
			if matches:
				print "{}{}{} Matches : {}\"{}\"{}".format(textcolor.BOLD, v, textcolor.RESET, textcolor.OKGREEN, i, textcolor.RESET)
				exec("output = {}_messageHandler(msg, matches)".format(v))
				if output:
					bot.reply_to(msg, output, parse_mode="markDown")
@bot.callback_query_handler(func=lambda call: True)
def process_callback(call):
	if is_banned(call.from_user.id):
			return
	print """#Callback\n[{}]
[{}] -> \"{}\"""".format(datetime.now().strftime("%Y/%m/%d - %H:%M"), call.from_user.first_name.encode("utf-8"), call.data.encode("utf-8"))
	patterns = []
	for v in working_plugins:
		try:
			exec("patterns = plugin_{}.callback_patterns".format(v))
		except:
			pass
		for i in patterns:
			#matches = re.match(i, msg.text)
			exec("matches = re.match(r'{}', call.data)".format(i))
			if matches:
				print "{}{}{} CallbackMatches : {}\"{}\"{}".format(textcolor.BOLD, v, textcolor.RESET, textcolor.OKGREEN, i, textcolor.RESET)
				exec("output = {}_callbackHandler(call, matches)".format(v))
				if output:
					bot.answer_callback_query(call.id, text=output)
@bot.inline_handler(func=lambda query: True)
def process_inline(inline_query):
	if is_banned(inline_query.from_user.id):
			return
	print """#Inline\n[{}]
[{}] -> \"{}\"""".format(datetime.now().strftime("%Y/%m/%d - %H:%M"), inline_query.from_user.first_name.encode("utf-8"), inline_query.query.encode("utf-8"))
	patterns = []
	for v in working_plugins:
		try:
			exec("patterns = plugin_{}.inline_patterns".format(v))
		except:
			pass
		for i in patterns:
			#matches = re.match(i, msg.text)
			exec("matches = re.match(r'{}', inline_query.query)".format(i))
			if matches:
				print "{}{}{} InlineMatches : {}\"{}\"{}".format(textcolor.BOLD, v, textcolor.RESET, textcolor.OKGREEN, i, textcolor.RESET)
				try:
					exec("output = {}_inlineHandler(inline_query, matches)".format(v))
				except:
					pass
				if output:
					try:
						count = 1
						answers = []
						for i in output:
							exec("r{} = types.InlineQueryResultArticle(str(i[{}]['id']), i[{}]['label'], types.InputTextMessageContent(i[{}]['content'], parse_mode='markDown'), description=i[{}]['description'], thumb_url=i[{}]['thumb_url'])".format(count, count-1,  count-1, count-1, count-1, count-1))
							count += 1
							exec("name = r{}".format(count-1))
							answers.append(name)
					except Exception as e:
						print sys.exc_info()[-1].tb_lineno
						print "{}{}{}".format(textcolor.FAIL, e, textcolor.RESET)
						pass
					bot.answer_inline_query(inline_query.id, answers)
@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_member", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id", "pinned_message"])
def process_message_types(msg):
	if msg.caption:
		msg.text = "{}_{}".format(msg.content_type, msg.caption.encode("utf-8"))
	else:
		msg.text = msg.content_type
	if msg.chat.type == "private":
		print """#Message\n[{}]
[{}] -> \"{}\"""".format(datetime.now().strftime("%Y/%m/%d - %H:%M"), msg.from_user.first_name.encode("utf-8"), msg.text.encode("utf-8"))

		if is_banned(msg.from_user.id):
			return
	if msg.chat.type != "private":
		print """#Message\n[{}]
[{}] - [{}] -> \"{}\"
""".format(datetime.now().strftime("%Y/%m/%d - %H:%M"), msg.from_user.first_name.encode("utf-8"), msg.chat.title.encode("utf-8"), msg.text.encode("utf-8"))
	patterns = []
	for v in working_plugins:
		try:
			exec("patterns = plugin_{}.patterns".format(v))
		except:
			pass
		
		for i in patterns:
			#matches = re.match(i, msg.text)
			exec("matches = re.match(r'{}', msg.text)".format(i))
			if matches:
				print "{}{}{} Matches : {}\"{}\"{}".format(textcolor.BOLD, v, textcolor.RESET, textcolor.OKGREEN, i, textcolor.RESET)
				exec("output = {}_messageHandler(msg, matches)".format(v))
				if output:
					bot.reply_to(msg, output, parse_mode="markDown")
@bot.edited_message_handler(func=lambda message: True)
def process_edites(msg):
	process_messages(msg)
@bot.channel_post_handler(func=lambda message: True)
def process_channel_messages(msg):
	process_messages(msg)

bot.polling()
