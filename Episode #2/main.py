import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=[1234567890])


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.slash_command()
async def ping(interaction):
    await interaction.response.send_message("Pong!")

bot.run("token")
