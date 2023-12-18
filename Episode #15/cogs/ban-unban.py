# Импортируем необходимые модули из библиотеки disnake.
import disnake
from disnake.ext import commands


# Определяем класс "Ban", который является расширением (Cog) для бота.
class Ban(commands.Cog):
    # Инициализируем класс "Ban" и сохраняем объект бота в атрибуте "self.bot".
    def __init__(self, bot):
        self.bot = bot

    # Создаем слэш-команду "ban", которая будет выполняться при вызове.
    @commands.slash_command()
    async def ban(self, interaction, user: disnake.User, reason: str):
        # Выполняем бан пользователя на сервере с указанным поводом (reason).
        await interaction.guild.ban(user, reason=reason)
        # Отправляем эфемеральное сообщение с информацией о бане.
        await interaction.response.send_message(
            f"Пользователь {user.mention} был забанен по причине: {reason}",
            ephemeral=True
        )

    # Создаем слэш-команду "un_ban", которая будет выполняться при вызове.
    @commands.slash_command()
    async def un_ban(self, interaction, user: disnake.User):
        # Убираем бан с указанного пользователя на сервере.
        await interaction.guild.unban(user)
        # Отправляем эфемеральное сообщение с информацией об удалении бана.
        await interaction.response.send_message(
            f"Пользователь {user.mention} был разбанен.",
            ephemeral=True
        )


# Функция setup, которая добавляет класс Ban как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Ban(bot))
