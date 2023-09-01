# Импортируем необходимые модули из библиотеки Disnake.
import disnake
from disnake.ext import commands


# Определяем класс "Ping", который является расширением (Cog) для бота.
class Ping(commands.Cog):
    # Инициализируем класс "Ping" и сохраняем объект бота в атрибуте "self.bot".
    def __init__(self, bot):
        self.bot = bot

    # Определяем метод "ping", который будет вызываться при выполнении команды "/ping".
    # Он отправляет сообщение "Pong!" в ответ на взаимодействие (interaction).
    @commands.slash_command()
    async def ping(self, interaction: disnake.CommandInteraction):
        await interaction.response.send_message("Pong!")


# Определяем функцию "setup", которая добавляет расширение "Ping" в бота.
def setup(bot):
    bot.add_cog(Ping(bot))
