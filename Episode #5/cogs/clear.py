# Импортируем необходимые модули из библиотеки disnake.
import disnake
from disnake.ext import commands


# Определяем класс "Clear", который является расширением (Cog) для бота.
class Clear(commands.Cog):
    # Инициализируем класс "Clear" и сохраняем объект бота в атрибуте "self.bot".
    def __init__(self, bot):
        self.bot = bot

    # Создаем слэш-команду "clear", которая будет выполняться при вызове.
    @commands.slash_command()
    async def clear(self, interaction, amount: int):
        # Создаем эмбед (вложенное сообщение) с информацией о количестве удаленных сообщений.
        embed = disnake.Embed(title="Clear", description=f"Deleted {amount} messages", color=0x00ff00)
        # Устанавливаем миниатюру (thumbnail) для эмбеда, используя URL аватара бота.
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        # Отправляем эмбед как ответ на взаимодействие (interaction), сделав его эфемеральным (исчезающим).
        await interaction.response.send_message(embed=embed, ephemeral=True)
        # Удаляем сообщения в текущем канале, включая вызванную команду, в количестве "amount + 1".
        await interaction.channel.purge(limit=amount + 1)


# Функция setup, которая добавляет класс Clear как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Clear(bot))
