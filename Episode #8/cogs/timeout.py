# Импортируем необходимые модули из библиотеки disnake и datetime.
import datetime

import disnake
from disnake.ext import commands


# Определяем класс "Timeout", который является расширением (Cog) для бота.
class Timeout(commands.Cog):
    # Инициализируем класс "Timeout" и сохраняем объект бота в атрибуте "self.bot".
    def __init__(self, bot):
        self.bot = bot

    # Создаем слэш-команду "timeout", которая будет выполняться при вызове.
    @commands.slash_command()
    async def timeout(self, interaction, member: disnake.Member, time: int, reason: str):
        # Проверяем, что автор команды не пытается замутить самого себя.
        if member == interaction.author:
            return await interaction.response.send_message(
                "You can't time out yourself",
                ephemeral=True
            )

        # Проверяем, что время мута не может быть меньше 1 минуты.
        if time < 1:
            return await interaction.response.send_message(
                "Time can't be less than 1 minute",
                ephemeral=True
            )

        # Вычисляем время окончания таймаута, добавляя указанное количество минут к текущему времени.
        time = datetime.datetime.now() + datetime.timedelta(minutes=time)
        # Применяем таймаут к указанному пользователю с заданным временем и причиной.
        await member.timeout(until=time, reason=reason)
        # Форматируем время окончания мута для удобного отображения.
        cool_time = disnake.utils.format_dt(time, style="R")
        # Создаем эмбед (вложенное сообщение) с информацией о наложенном таймауте.
        embed = disnake.Embed(
            title="Timeout",
            description=f"{member.mention} has been timed out {cool_time} for {reason}",
            color=0x2F3136
        ).set_thumbnail(url=member.display_avatar.url)
        # Отправляем эмбед как ответ на взаимодействие (interaction), сделав его эфемеральным (исчезающим).
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Создаем слэш-команду "un_timeout", которая будет выполняться при вызове.
    @commands.slash_command()
    async def un_timeout(self, interaction, member: disnake.Member):
        # Убираем таймаут с указанного пользователя.
        await member.timeout(until=None, reason=None)
        # Отправляем эфемеральное сообщение с информацией об удалении таймаута.
        await interaction.response.send_message(
            f"Untimed out {member.mention}",
            ephemeral=True
        )


# Функция setup, которая добавляет класс Timeout как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Timeout(bot))
