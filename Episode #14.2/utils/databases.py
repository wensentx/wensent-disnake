# Импортируем необходимые модули.
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
                query = '''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    money INTEGER,
                    premium INTEGER
                )'''
                await cursor.execute(query)
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