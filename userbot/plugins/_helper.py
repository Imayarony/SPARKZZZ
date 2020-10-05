from userbot import CMD_LIST
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd
from platform import uname
import sys
from telethon import events, functions, __version__

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "SPARKZZZ user"

@sparkzzz.on(admin_cmd(pattern="help ?(.*)"))
@sparkzzz.on(admin_cmd(pattern="help ?(.*)", allow_sudo=True))
async def cmd_list(event):
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        input_str = event.pattern_match.group(1)
        if tgbotusername is None or input_str == "text":
            string = ""
            for i in CMD_LIST:
                string += "⚡" + i + "\n"
                for iter_list in CMD_LIST[i]:
                    string += "    `" + str(iter_list) + "`"
                    string += "\n"
                string += "\n"
            if len(string) > 4095:
                with io.BytesIO(str.encode(string)) as out_file:
                    out_file.name = "cmd.txt"
                    await bot.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="**COMMANDS**",
                        reply_to=reply_to_id
                    )
                    await event.delete()
            else:
                await event.reply(string)
        elif input_str:
            if input_str in CMD_LIST:
                string = "Commands found in {}:".format(input_str)
                for i in CMD_LIST[input_str]:
                    string += "    " + i
                    string += "\n"
                await event.reply(string)
            else:
                await event.reply(input_str + " is not a valid plugin!")
        else:
            help_string = f"Userbot Helper.. Provided by {DEFAULTUSER}\
                          \n`Userbot Helper for to reveal all the commands of `**[SPARKZZZ](https://github.com/vishnu175/SPARKZZZ/)**\
                          \n__Type__ `.help`<module name> to know usage of modules.__\
                          \nDo `.info` plugin_name for usage"
            results = await bot.inline_query(  # pylint:disable=E0602
                tgbotusername, help_string
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
                hide_via=True
            )
            await event.delete()
            
@sparkzzz.on(admin_cmd(pattern="dc"))  # pylint:disable=E0602
@sparkzzz.on(admin_cmd(pattern="dc", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())  # pylint:disable=E0602
    await event.reply(result.stringify())


@sparkzzz.on(admin_cmd(pattern="config"))  # pylint:disable=E0602
@sparkzzz.on(admin_cmd(pattern="config", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetConfigRequest())  # pylint:disable=E0602
    result = result.stringify()
    logger.info(result)  # pylint:disable=E0602
    await event.reply("""Telethon UserBot powered by SPARKZZZ UserBot""")


@sparkzzz.on(admin_cmd(pattern="syntax (.*)"))
@sparkzzz.on(admin_cmd(pattern="syntax (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    plugin_name = event.pattern_match.group(1)

    if plugin_name in CMD_LIST:
        help_string = CMD_LIST[plugin_name].__doc__
        unload_string = f"Use `.unload {plugin_name}` to remove this plugin.\n           © SPARKZZZ UserBot"
        
        if help_string:
            plugin_syntax = f"Syntax for plugin **{plugin_name}**:\n\n{help_string}\n{unload_string}"
        else:
            plugin_syntax = f"No DOCSTRING has been setup for {plugin_name} plugin."
    else:

        plugin_syntax = "Enter valid **Plugin** name.\nDo `.help` to get list of valid plugin names."

    await event.reply(plugin_syntax)
