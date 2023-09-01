# Импортируем необходимые модули из библиотеки disnake.
import disnake
from disnake.ext import commands


# Определяем класс "Avatar", который является расширением (Cog) для бота.
class Avatar(commands.Cog):
    # Инициализируем класс "Avatar" и сохраняем объект бота в атрибуте "self.bot".
    def __init__(self, bot):
        self.bot = bot

    # Создаем слэш-команду "avatar", которая будет выполняться при вызове.
    @commands.slash_command()
    async def avatar(self, interaction, member: disnake.Member = None):
        # Если не указан пользователь (member), используем автора команды.
        member = member or interaction.author
        # Создаем эмбед (вложенное сообщение) с информацией о аватаре пользователя.
        embed = disnake.Embed(
            title=f"Аватар – {member}",
            color=0x2F3136
        )
        # Устанавливаем изображение (аватар) в эмбед.
        embed.set_image(url=member.display_avatar)
        # Отправляем эмбед как ответ на взаимодействие (interaction).
        await interaction.response.send_message(embed=embed)


# Функция setup, которая добавляет класс Avatar как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Avatar(bot))
