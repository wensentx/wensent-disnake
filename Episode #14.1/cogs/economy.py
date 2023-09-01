import disnake
from disnake.ext import commands

from utils.databases import UsersDataBase


# Определяем класс "Economy", который является расширением (Cog) для бота.
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()  # Инициализируем объект базы данных для управления экономикой.

    # Создаем слэш-команду "баланс", которая позволяет пользователю посмотреть свой баланс.
    @commands.slash_command(name='баланс', description='Посмотреть баланс')
    async def balance(self, interaction, member: disnake.Member = None):
        await self.db.create_table()  # Создаем таблицу в базе данных, если она не существует.
        if not member:
            member = interaction.author  # Если не указан конкретный пользователь, используем автора команды.
        await self.db.add_user(member)  # Добавляем пользователя в базу данных, если его там нет.
        user = await self.db.get_user(member)  # Получаем данные о пользователе из базы данных.
        embed = disnake.Embed(color=0x2F3136, title=f'Баланс пользователя - {member}')
        embed.add_field(name=':coin: Деньги', value=f'```{user[1]}```')  # Отображаем количество денег пользователя.
        embed.add_field(name=':gem: Премиум', value=f'```{user[2]}```')  # Отображаем количество премиум-валюты.
        embed.set_thumbnail(url=member.display_avatar.url)  # Устанавливаем аватар пользователя.
        await interaction.response.send_message(embed=embed)  # Отправляем сообщение с балансом.

    # Создаем слэш-команду "выдать", которая позволяет выдать деньги или премиум пользователю.
    @commands.slash_command(name='выдать', description='Выдать деньги пользователю')
    async def give(self, interaction, member: disnake.Member, amount: int,
                   arg=commands.Param(choices=['деньги', 'премиум'])):
        # ВНИМАНИЕ: Если ввести отрицательное число (amount), то из баланса пользователя вычтется указанное количество.
        await self.db.create_table()  # Создаем таблицу в базе данных, если она не существует.
        await self.db.add_user(member)  # Добавляем пользователя в базу данных, если его там нет.
        if arg == 'деньги':
            await self.db.update_money(member, amount, 0)  # Обновляем количество денег пользователя.
            embed = disnake.Embed(color=0x2F3136, title=f'Выдача денег пользователю - {member}')
            embed.description = f'{interaction.author.mention} выдал {member.mention} {amount} денег.'
        else:
            await self.db.update_money(member, 0, amount)  # Обновляем количество премиум-валюты пользователя.
            embed = disnake.Embed(color=0x2F3136, title=f'Выдача премиума пользователю - {member}')
            embed.description = f'{interaction.author.mention} выдал {member.mention} {amount} премиума.'
        embed.set_thumbnail(url=member.display_avatar.url)  # Устанавливаем аватар пользователя.
        await interaction.response.send_message(embed=embed)  # Отправляем сообщение о выдаче.


# Функция setup, которая добавляет класс Economy как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Economy(bot))
