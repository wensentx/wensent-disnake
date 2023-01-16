import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


bot.run("token")
