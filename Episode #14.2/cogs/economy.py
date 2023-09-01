# Импортируем необходимые модули из библиотеки disnake и из файла utils.databases.
import disnake
from disnake.ext import commands
from utils.databases import UsersDataBase


# Определяем класс "PaginatorView", который расширяет функциональность кнопок визуального интерфейса.
class PaginatorView(disnake.ui.View):
    def __init__(self, embeds, author, footer: bool, timeout=30.0):
        self.embeds = embeds  # Список эмбедов для отображения.
        self.author = author  # Автор сообщения.
        self.footer = footer  # Флаг для отображения подвала с номером страницы.
        self.timeout = timeout  # Время ожидания в секундах для автоматической очистки интерфейса.
        self.page = 0  # Текущая страница (индекс) из списка эмбедов.
        super().__init__(timeout=self.timeout)

        # Если флаг footer установлен, то добавляем номер страницы в подвал каждого эмбеда.
        if self.footer:
            for emb in self.embeds:
                emb.set_footer(text=f'Страница {self.embeds.index(emb) + 1} из {len(self.embeds)}')

    # Создаем кнопку "Назад" со стрелкой влево.
    @disnake.ui.button(label='◀️', style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        # Проверяем, что автор кнопки совпадает с автором интерфейса.
        if self.author.id == interaction.author.id:
            if self.page == 0:  # Если текущая страница - первая, перейдем на последнюю.
                self.page = len(self.embeds) - 1
            else:
                self.page -= 1  # В противном случае перейдем на предыдущую страницу.
        else:
            return

        await self.button_callback(interaction)

    # Создаем кнопку "Вперед" со стрелкой вправо.
    @disnake.ui.button(label='▶️', style=disnake.ButtonStyle.grey)
    async def next(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        # Проверяем, что автор кнопки совпадает с автором интерфейса.
        if self.author.id == interaction.author.id:
            if self.page == len(self.embeds) - 1:  # Если текущая страница - последняя, перейдем на первую.
                self.page = 0
            else:
                self.page += 1  # В противном случае перейдем на следующую страницу.
        else:
            return

        await self.button_callback(interaction)

    # Обработчик нажатия кнопки, который отображает соответствующий эмбед.
    async def button_callback(self, interaction):
        # Проверяем, что автор кнопки совпадает с автором интерфейса.
        if self.author.id == interaction.author.id:
            await interaction.response.edit_message(embed=self.embeds[self.page])
        else:
            return await interaction.response.send_message('Вы не можете использовать эту кнопку!', ephemeral=True)


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
        embed.add_field(name=':money: Деньги', value=f'```{user[1]}```')  # Отображаем количество денег пользователя.
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

    # Создаем слэш-команду "топ", которая позволяет посмотреть топ пользователей.
    @commands.slash_command(name='топ', description='Посмотреть топ пользователей')
    async def top(self, interaction):
        await self.db.create_table()  # Создаем таблицу в базе данных, если она не существует.
        top = await self.db.get_top()  # Получаем топ пользователей из базы данных.
        embeds = []  # Здесь создается пустой список embeds, который будет
        # содержать эмбеды для каждой страницы топ-пользователей.

        #  Эти переменные используются для отслеживания текущего номера пользователя в топе (n)
        #  и количества пользователей, добавленных на текущей странице (loop_count).
        loop_count = 0
        n = 0
        # Эта строка создает пустую строку text,
        # которая будет содержать текстовое представление пользователей на текущей странице.
        text = ''
        # Этот код начинает цикл, в котором мы перебираем пользователей из списка top
        for user in top:
            # При каждой итерации увеличивается переменная n, чтобы отслеживать текущий номер пользователя.
            n += 1
            # Этот счетчик используется для определения, сколько пользователей добавлено на текущей странице.
            loop_count += 1
            # Здесь мы создаем строку, которая представляет информацию о пользователе.
            # Мы используем форматирование строк (f-строки), чтобы вставить номер пользователя (n),
            # имя пользователя (self.bot.get_user(user[0])), и его баланс (user[1]).
            # Также мы добавляем смайлик :coin: для обозначения валюты.
            text += f'**{n}.** {self.bot.get_user(user[0])} - {user[1]} :coin:\n'
            # Этот код проверяет, сколько пользователей было добавлено на текущей странице.
            # Если добавлено 10 пользователей (loop_count % 10 == 0) или это последний пользователь в
            # списке (loop_count - 1 == len(top) - 1), то это означает, что текущая страница завершена.
            if loop_count % 10 == 0 or loop_count - 1 == len(top) - 1:
                # Здесь мы создаем объект эмбеда с указанным цветом и заголовком для текущей страницы.
                embed = disnake.Embed(color=0x2F3136, title='Топ пользователей')
                # Здесь мы устанавливаем описание эмбеда, которое содержит текстовое представление пользователей.
                embed.description = text
                # Мы устанавливаем миниатюру эмбеда равной аватару пользователя, который вызвал команду.
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                # Мы добавляем эмбед в список embeds.
                embeds.append(embed)
                # Мы сбрасываем значение переменной text, чтобы начать новую страницу.
                text = ''
        #  Здесь создается объект PaginatorView, который будет использоваться для интерактивной пагинации.
        #  Мы передаем список эмбедов (embeds), автора команды (interaction.author) и флаг True, который указывает,
        #  что на странице есть футер с номером страницы.
        view = PaginatorView(embeds, interaction.author, True)
        # Мы отправляем первый эмбед из списка embeds вместе с объектом PaginatorView в ответ на команду.
        # Это создает интерактивное сообщение с возможностью переключения между
        # страницами топ-пользователей при помощи кнопок "◀️" и "▶️".
        await interaction.response.send_message(embed=embeds[0], view=view)


# Функция setup, которая добавляет класс Economy как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Economy(bot))
