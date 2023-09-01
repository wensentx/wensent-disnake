# Импортируем необходимые модули из библиотеки Disnake.
from disnake.ext import commands


# Определяем класс "Clear", который является расширением (Cog) для бота.
class Clear(commands.Cog):
    # Инициализируем класс "Clear" и сохраняем объект бота в атрибуте "self.bot".
    def __init__(self, bot):
        self.bot = bot

    # Создаем слэш-команду "clear", которая будет выполняться при вызове.
    @commands.slash_command()
    async def clear(self, interaction, amount: int):
        # Отправляем эфемерное (исчезающее) сообщение с информацией о количестве удаленных сообщений.
        await interaction.response.send_message(f"Deleted {amount} messages", ephemeral=True)
        # Удаляем сообщения в текущем канале, включая вызванную команду, в количестве "amount + 1".
        await interaction.channel.purge(limit=amount + 1)


# Функция setup, которая добавляет класс Clear как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Clear(bot))