def help_messageHandler(msg, matches):
	output = "*Plugin List:*\n"
	for v in working_plugins:
		try:
			exec("helptext = plugin_{}.helpText".format(v))
			exec("pluginname = plugin_{}.pluginName".format(v))
			exec("helpcommand = plugin_{}.helpCommand".format(v))
			output += """\n*{}*
`{}`
{}\n""".format(pluginname, helpcommand, helptext)
			splitted_text = util.split_string(output, 3000)
		except:
			pass
	for text in splitted_text:
		bot.reply_to(msg, output, parse_mode="markDown")
class plugin_help:
	patterns = ["[!/#]help$"]
	
	pluginName = "Help"
	helpCommand = "/help"
	helpText = "to get help text"
