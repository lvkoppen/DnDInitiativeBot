import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

private_tkn = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')
init_roller_timer_in_seconds = 30
party_max = 5

players = []

# TODO: change player list to dict, add clear after new ini roll start, if assigned value changed since last checked, update else ignore

init_msg = None


@bot.event
async def on_ready():
    print("Bot is ready")


# function to register players in a global array
# function to check if all players responded within msg history

# register a player
@bot.command(name="reg")
async def register_player(ctx):
    if len(players) >= party_max:
        await ctx.send('the party is full.')
        await ctx.send(get_party_list())
        return
    elif not ctx.author in players:
        players.append(ctx.author)
        print(f"Adding {ctx.author.display_name} to playerlist")
        await ctx.send('Succesfully registered to the party!')
    else:
        print(f"{ctx.author.display_name} is already in the list, ignoring")
        await ctx.send(f'No need to register again {ctx.author.display_name} :)')

# obtain registered players


@bot.command(name="players")
@commands.has_role("DungeonMaster")
async def show_registered_players(ctx):
    await ctx.send(get_party_list())


@bot.command(name="sp_max")
@commands.has_role("DungeonMaster")
async def show_registered_players(ctx, args):
    global party_max
    try:
        party_max = int(args)
    except:
        await ctx.send('Invalid number!')
    await ctx.send(f"The party max is set to {party_max}")


@bot.command(name="get_partymax_size")
async def max_party_size(ctx):
    await ctx.send(party_max)


@bot.command(name="clear")
@commands.has_role("DungeonMaster")
async def show_registered_players(ctx):
    global players
    players = []
    await ctx.send("Cleared player list!")


def get_party_list():
    string_msg = "The following players are registered: \n"
    for player in players:
        string_msg += f"{player.display_name}\n"
    return string_msg


@bot.command(name="set_ini")
@commands.has_role("DungeonMaster")
async def start_init_roller(ctx, args):
    global init_roller_timer_in_seconds
    try:
        init_roller_timer_in_seconds = int(args)
        await ctx.send(f'Timer has been set to {init_roller_timer_in_seconds} seconds')
    except:
        await ctx.send('Should be a number!')  # is gewoon een failsafe :shrug:


async def players_answered():
    # TODO check if all players answered based on message history
    # or register every user in a dictionary along with their init roll

    # h_messages = await init_msg.channel.history().flatten()
    # player_list = players
    # for h_msg in h_messages:
    #     if h_msg.author in player_list:
    #         player_list[h_msg.author] = None

    # if len(player_list) > 0:
    #     return False

    # return True
    pass


@bot.command(name="ini")
@commands.has_role("DungeonMaster")
async def start_init_roller(ctx):
    global init_msg

    if not init_msg == None:  # make sure a second timer doesn't spawn
        return

    # should prob register channel somewhere
    channel = bot.get_channel(875667641753276426)

    init_msg = await channel.send("Starting countdown!")

    counter = init_roller_timer_in_seconds
    while True:
        counter -= 1
        if counter <= 0:
            await init_msg.edit(content="Countdown has ended!")
            break
        if await players_answered():
            await init_msg.edit(content="All players answered!")
            break
        # if all players have answered break loop
        await init_msg.edit(content=f"Time left to roll: {counter}")

    init_msg = None
    # channel = bot.get_channel(875667641753276426)  # get Dice Roll channel

    # await ctx.send(f'Starting countdown in {channel.name}')
    # msg = await channel.send('Starting countdown!')
    # secondint = init_roller_timer_in_seconds  # magic number i know but screw it
    # while True:
    #     secondint -= 1
    #     if secondint <= 0:
    #         # edit existing message
    #         await msg.edit(content="countdown has ended!")
    #         break
    #     await msg.edit(content=f"Timer: {secondint}")
    #     # sleeps for 1 second, not best method to use but idk what else yet
    #     await asyncio.sleep(1)

    # messages = await msg.channel.history(after=msg).flatten()

    # await ctx.send()
    # for messig in messages:
    #     print(messig.content)


bot.run(private_tkn)
