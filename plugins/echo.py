def echo_messageHandler(msg, matches):
	markup = types.InlineKeyboardMarkup()
	locks_bt = types.InlineKeyboardButton(":/", callback_data="/echo {}".format(matches.group(1)))
	markup.add(locks_bt)
	bot.send_message(msg.chat.id, matches.group(1), reply_markup=markup)
def echo_callbackHandler(call, matches):
	return "callback {}".format(matches.group(1))
def echo_inlineHandler(query, matches):
	try:
		r1= types.InlineQueryResultArticle("1", "Click Here", types.InputTextMessageContent(matches.group(1), parse_mode='markDown'), description="Click here to send your text with bold and ...", thumb_url="")
		bot.answer_inline_query(query.id, [r1])

	except Exception as e:
		print(e)
		r1= types.InlineQueryResultArticle("1", "Error", types.InputTextMessageContent("*Error*", parse_mode='markDown'), description="Error", thumb_url="")
		bot.answer_inline_query(query.id, [r1])


class plugin_echo:
	patterns = ["[!/#]echo (.*)"]
	callback_patterns = ["[!/#]echo (.*)"]
	inline_patterns = ["[!/#]echo (.*)"]
	
	pluginName = "Echo"
	helpCommand = "/echo <text>"
	helpText = "to get \"<text>\" from bot"
	
	
	
