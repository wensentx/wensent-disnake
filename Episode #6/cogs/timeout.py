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
        # Вычисляем время окончания таймаута, добавляя указанное количество минут к текущему времени.
        time = datetime.datetime.now() + datetime.timedelta(minutes=time)
        # Применяем таймаут к указанному пользователю с заданным временем и причиной.
        await member.timeout(until=time, reason=reason)
        # Отправляем эфемеральное сообщение с информацией о наложенном таймауте.
        await interaction.response.send_message(
            f"Пользователь {member.mention} был затайм-аутен до {time.strftime('%H:%M:%S %d.%m.%Y')}",
            ephemeral=True
        )

    # Создаем слэш-команду "un_timeout", которая будет выполняться при вызове.
    @commands.slash_command()
    async def un_timeout(self, interaction, member: disnake.Member):
        # Убираем таймаут с указанного пользователя.
        await member.timeout(until=None, reason=None)
        # Отправляем эфемеральное сообщение с информацией об удалении таймаута.
        await interaction.response.send_message(
            f"Пользователь {member.mention} был разтайм-аутен",
            ephemeral=True
        )


# Функция setup, которая добавляет класс Timeout как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Timeout(bot))
