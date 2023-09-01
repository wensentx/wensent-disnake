# Импортируем необходимые модули из библиотеки Disnake.
import disnake
from disnake.ext import commands


# Определяем класс "Embed", который является расширением (Cog) для бота.
class Embed(commands.Cog):
    # Инициализируем класс "Embed" и сохраняем объект бота в атрибуте "self.bot".
    def __init__(self, bot):
        self.bot = bot

    # Создаем слэш-команду "embed", которая будет выполняться при вызове команды "/embed".
    @commands.slash_command()
    async def embed(self, interaction):
        # Создаем вложенный объект Embed (эмбед)
        embed = disnake.Embed(title="Embed Title", description="Embed Description", color=0x00ff00)
        # Добавляем три поля в эмбед с соответствующими названиями и значениями
        embed.add_field(name="Field 1", value="Value 1", inline=False)
        embed.add_field(name="Field 2", value="Value 2", inline=False)
        embed.add_field(name="Field 3", value="Value 3", inline=False)
        # Устанавливаем текст для нижнего колонтитула (footer) эмбеда
        embed.set_footer(text="Embed Footer")
        # Устанавливаем имя автора эмбеда
        embed.set_author(name="Embed Author")
        # Устанавливаем миниатюру (thumbnail) для эмбеда, используя URL аватара бота
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        # Устанавливаем изображение (image) для эмбеда, также используя URL аватара бота
        embed.set_image(url=self.bot.user.avatar.url)
        # Отправляем сообщение с вложенным эмбедом в ответ на взаимодействие (interaction)
        await interaction.response.send_message(embed=embed)


# Определяем функцию "setup", которая добавляет расширение "Clear" в бота.
def setup(bot):
    bot.add_cog(Embed(bot))
