#  Импортируются необходимые модули
import disnake
from disnake.ext import commands

#  Создается объект intents, который включает все разрешения для бота.
#  Создается экземпляр класса Bot с префиксом команд "!" и указанными разрешениями.
intents = disnake.Intents.all()  # Подключаем все разрешения
bot = commands.Bot(command_prefix="!", intents=intents)


# Определяется функция on_ready, которая будет вызываться, когда бот будет готов к использованию.
# В данном случае, она просто выводит сообщение "Bot is ready!" в консоль.
@bot.event
async def on_ready():
    print("Bot is ready!")


# Определяется команда ping, которая отправляет сообщение "Pong!" в ответ на команду "!ping".
@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")


# Запускается бот с помощью метода run, передавая ему токен для авторизации.
bot.run("token")
