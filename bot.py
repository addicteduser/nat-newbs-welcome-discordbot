import os
import discord
import asyncio
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
        await bot_typing(ctx, 5)
        await ctx.send(f'Apologies, Master {ctx.author.mention}. I am but a simple AI. '
                       'I don\'t know how to respond to that at the moment. Perhaps my human consciousness '
                       f'{get_human_welcome_wagon(ctx.guild).mention} knows how.')


# def log_error(error, msg):
#     print(f'ERROR: {error}')
#     print(f'COMMAND: {msg}')

@bot.event
async def on_member_join(member):
    channel_welcome = get(member.guild.channels, name="welcome")
    await bot_typing(ctx, 3)
    await channel_welcome.send(get_welcome_message(member.guild, [member]))


##################
## BOT COMMANDS ##
##################
@bot.command()
async def greet(ctx, members: commands.Greedy[discord.Member] = None, *args):
    await bot_typing(ctx, 5)
    await ctx.send(get_welcome_message(ctx.guild, members))


@bot.command()
async def vault(ctx):
    await bot_typing(ctx, 5)
    await ctx.send(
        f'Salutations, Master {ctx.author.mention}. Here is the link to '
        '__**The Natural Newbie Vault**__: https://app.roll20.net/join/7260172/yvr0fg. '
        'Feel free to use it as a character vault. Just ask any of our ~~overlords~~, '
        'I mean, Admins and Dungeon Masters, to make a folder for you and/or '
        'provide you with more blank character sheets.')


@bot.command()
async def hello(ctx):
    await bot_typing(ctx, 3)
    await ctx.send(get_greetings(ctx))


@bot.command()
async def hi(ctx):
    await bot_typing(ctx, 3)
    await ctx.send(get_greetings(ctx))


@bot.command()
async def henlo(ctx):
    await bot_typing(ctx, 3)
    await ctx.send(get_greetings(ctx))


@bot.command()
async def hewwo(ctx):
    await bot_typing(ctx, 3)
    await ctx.send(get_greetings(ctx))


######################
## HELPER FUNCTIONS ##
######################
async def bot_typing(ctx, time):
    await ctx.trigger_typing()
    await asyncio.sleep(time)


def get_greetings(ctx):
    return f'{ctx.command.name.capitalize()}, Master {ctx.author.mention}! :smile:'


def get_human_welcome_wagon(guild):
    return get(guild.members, name='chefcy2017')


def get_welcome_message(guild, members):
    channel_about = get(guild.channels, name='about')
    channel_server_guide = get(guild.channels, name='server-guide')

    welcome_message = ''

    if members is not None:
        newbies = ", ".join(newb.mention for newb in members)
        welcome_message = f'Greetings, {newbies}! '

    welcome_message = welcome_message + \
        f'Welcome to the __**Natural Newbie**__ server! I am `Welcome Wagon`, ' + \
        'the server\'s semi-sentient Help AI. As such, I advise you to please ' + \
        f'head to {channel_about.mention} in order to get started. ' + \
        f'If you are lost, kindly refer to the {channel_server_guide.mention}. ' + \
        'You may also seek assisstance from my human consciousness, aka ' + \
        f'"Jed" ({get_human_welcome_wagon(guild).mention}).'

    return welcome_message


if __name__ == '__main__':
    bot.run(token)
