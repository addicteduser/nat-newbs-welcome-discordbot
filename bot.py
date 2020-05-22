import os
import discord
from discord.ext import commands
from discord.utils import get

# for local development
# from secrets import DISCORD_TOKEN
# token = DISCORD_TOKEN

# for deployment
token = os.environ['DISCORD_TOKEN']


bot = commands.Bot(command_prefix=commands.when_mentioned,
                   case_insensitive=True,
                   description='Natural Newbies server\'s personal welcome bot.',
                   help_command=None)

#######################
## DISCORD BOT START ##
#######################


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    print('Connected to the following Discord servers: ')
    for guild in bot.guilds:
        print(f' >> {guild.name}')

#########################
## DISCORD BOT LOGGING ##
#########################


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandError):
        await ctx.send(f'Apologies, Master {ctx.author.mention}. I am but a simple AI. '
                       'I don\'t know how to respond to that at the moment. Perhaps my human consciousness '
                       f'{get_human_welcome_wagon(ctx.guild).mention} knows how.')


# def log_error(error, msg):
#     print(f'ERROR: {error}')
#     print(f'COMMAND: {msg}')

@bot.event
async def on_member_join(member):
    channel_lobby = get(member.guild.channels, name="lobby")
    await channel_lobby.send(get_welcome_message(member.guild, [member]))

##################
## BOT COMMANDS ##
##################


@bot.command()
async def greet(ctx, members: commands.Greedy[discord.Member] = None, *args):
    await ctx.send(get_welcome_message(ctx.guild, members))


def get_human_welcome_wagon(guild):
    return get(guild.members, name='chefcy2017')


def get_welcome_message(guild, members):
    role_admin = get(guild.roles, name='@Admin')
    role_dm = get(guild.roles, name='Dungeon Masters')

    channel_server_guide = get(guild.channels, name='server-guide')
    channel_tutorial = get(
        guild.channels, name='seeking-help-and-tutorial')
    channel_concept = get(guild.channels, name='concept')
    channel_lfg = get(guild.channels, name='looking-for-games')
    channel_lfp = get(guild.channels, name='looking-for-players')
    channel_game_sched = get(guild.channels, name='game-schedule')
    channel_roll20 = get(guild.channels, name='roll20-guides')

    welcome_message = ''

    if members is not None:
        newbies = ", ".join(newb.mention for newb in members)
        welcome_message = f'Hello, {newbies}!\n\n'

    welcome_message = welcome_message + \
        f'Welcome to the Natural Newbie server! I am `Welcome Wagon`, the server\'s semi-sentient Help AI. As such, I advise you to please head to {channel_server_guide.mention} in order to get started. You may also call my human consciousness, aka {get_human_welcome_wagon(guild).mention}, "Jed".\n\n' + \
        f'There is the {channel_tutorial.mention} for D&D-related questions that my human consciousness, the {role_admin.mention}, and the {role_dm.mention} would be happy to answer. It\'s there that you can also find the Adventurers League Players Guide (ALPG) in the pinned messages. That file contains all the information needed to create an AL-legal character. {channel_concept.mention} is the place where you can seek the wisdom and insight of the seasoned players and DMs on how to progress a specific character concept and build.\n\n' + \
        f'{channel_game_sched.mention} lists the upcoming games for the week. To discuss these, kindly head to {channel_lfg.mention}. Just above it is {channel_lfp.mention} where DMs post their scheduled sessions. Most games on this server are for characters from level 1-4 (Tier 1). On occasion, higher-tier games are run to show the newbies how more experienced players handle adventures of higher difficulty. {channel_roll20.mention} is where you may find essential information on using Roll20 properly, although you may still ask questions if you have any.\n\n' + \
        f'Feel free to use __**The Natural Newbie Vault**__ (https://app.roll20.net/join/7260172/yvr0fg) as a character vault. Just ask any of our ~~overlords~~, I mean, {role_admin.mention} and {role_dm.mention}, to make a folder for you and/or import your character/s from other Roll20 rooms.'

    return welcome_message


if __name__ == '__main__':
    bot.run(token)
