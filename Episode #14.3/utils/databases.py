# Импортируем необходимые модули.
import datetime

import aiosqlite
import disnake


# Определяем класс "UsersDataBase" для работы с базой данных пользователей.
class UsersDataBase:
    def __init__(self):
        self.name = 'dbs/users.db'  # Указываем путь к базе данных.

    # Метод "create_table" создает таблицу "users" в базе данных, если она не существует.
    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    money INTEGER,
                    premium INTEGER
                );
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    time TEXT NOT NULL,
                    description TEXT NOT NULL
                );
                '''
                await cursor.executescript(query)
            await db.commit()

    # Метод "get_user" получает данные пользователя из базы данных по его ID.
    async def get_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM users WHERE id = ?'
                await cursor.execute(query, (user.id,))
                return await cursor.fetchone()

    # Метод "add_user" добавляет пользователя в базу данных, если его там нет.
    async def add_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_user(user):
                async with db.cursor() as cursor:
                    query = 'INSERT INTO users (id, money, premium) VALUES (?, ?, ?)'
                    await cursor.execute(query, (user.id, 0, 0))
                    await db.commit()

    # Метод "update_money" обновляет количество денег и премиум-валюты у пользователя.
    # ВНИМАНИЕ: Если ввести отрицательное число (money или premium), то из баланса пользователя
    # вычтется указанное количество.
    async def update_money(self, user: disnake.Member, money: int, premium: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET money = money + ?, premium = premium + ? WHERE id = ?'
                await cursor.execute(query, (money, premium, user.id))
                await db.commit()

    # Метод "get_top" возвращает список пользователей, отсортированный по количеству денег.
    async def get_top(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM users ORDER BY money DESC'
                await cursor.execute(query)
                return await cursor.fetchall()

    # Методы для работы с транзакциями.
    # Метод получения транзакций пользователя
    async def get_transactions(self, user_id: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM transactions WHERE user_id = ?'
                await cursor.execute(query, (user_id,))
                return await cursor.fetchall()

    # Метод добавления транзакций пользователю
    async def add_transaction(self, user_id: int, amount: int, description: str):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'INSERT INTO transactions (user_id, amount, time, description) VALUES (?, ?, ?, ?)'
                await cursor.execute(query, (user_id, amount, datetime.datetime.now(), description))
                await db.commit()

    # Метод генерации эмбедов для истории транзакций
    async def get_embeds(self, interaction):
        data = await self.get_transactions(interaction.author.id)
        embeds = []
        n = 0
        loop_count = 0
        text = ""
        for row in data:
            n += 1
            time = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f')
            text += (f"{'➕' if row[2] > 0 else '➖'} **{abs(row[2])}** :coin:"
                     f"[{disnake.utils.format_dt(time, style='f')}]\n{row[4]}\n")
            loop_count += 1
            if loop_count % 10 == 0 or loop_count - 1 == len(data) - 1:
                embed = disnake.Embed(title=f"История транзакций {interaction.author.display_name}",
                                      description=text, color=0x2F3136)
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embeds.append(embed)
                text = ""
        return embeds
