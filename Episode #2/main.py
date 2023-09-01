#  Импортируются необходимые модули
import disnake
from disnake.ext import commands

#  Создается объект intents, который включает все разрешения для бота.
#  Создается экземпляр класса Bot с префиксом команд "!" и указанными разрешениями.
intents = disnake.Intents.all()  # Подключаем все разрешения
bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=[123456789])  # Вместо 1234567890 указать id сервера


# Определяется функция on_ready, которая будет вызываться, когда бот будет готов к использованию.
# В данном случае, она просто выводит сообщение "Bot is ready!" в консоль.
@bot.event
async def on_ready():
    print("Bot is ready!")


# Определяется команда ping в виде слеш-команды, которая отправляет сообщение "Pong!" в ответ на команду "/ping".
@bot.slash_command()
async def ping(interaction: disnake.CommandInteraction):
    await interaction.response.send_message(f"Pong!")


# Запускается бот с помощью метода run, передавая ему токен для авторизации.
bot.run("token")
