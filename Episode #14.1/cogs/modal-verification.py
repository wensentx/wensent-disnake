# Импортируем необходимые модули из библиотеки disnake.
import disnake
from disnake.ext import commands

# Определяем класс "VerifyModal", который наследуется от disnake.ui.Modal.
class VerifyModal(disnake.ui.Modal):
    def __init__(self, code):
        self.code = code

        # Создаем компонент ввода текста (TextInput) для ввода верификационного кода.
        components = [
            disnake.ui.TextInput(label="Введите код", placeholder=str(self.code), custom_id="code")
        ]

        super().__init__(title="Верификация", components=components, custom_id="verify_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        # Проверяем введенный пользователем код с верификационным кодом.
        if self.code == int(interaction.text_values["code"]):
            role = interaction.guild.get_role(...)  # Получаем роль не верифицированного пользователя
            await interaction.author.remove_roles(role)  # Убираем роль не верифицированного пользователя
            await interaction.response.send_message("Вы успешно прошли верификацию!", ephemeral=True)
        else:
            await interaction.response.send_message("Неверный код!", ephemeral=True)


# Определяем класс "ButtonView", который наследуется от disnake.ui.View.
class ButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Верификация", style=disnake.ButtonStyle.grey, custom_id="button1")
    async def button1(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        import random
        code = random.randint(1000, 9999)  # Генерируем случайный верификационный код
        await interaction.response.send_modal(VerifyModal(code))


# Определяем класс "Verify", который является расширением (Cog) для бота.
class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    # Создаем команду "verify", которая будет выводить сообщение с кнопкой для верификации.
    @commands.command()
    async def verify(self, ctx):
        embed = disnake.Embed(color=0x2F3136)
        embed.set_image(url='https://i.imgur.com/2vWxaNL.png')  # Устанавливаем изображение в эмбеде
        await ctx.send(embed=embed, view=ButtonView())  # Отправляем эмбед с кнопкой для верификации

    # Создаем слушателя события "on_ready", который добавляет персистентное меню выбора ролей.
    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added:
            return

        # Message ID сообщения, где будет кнопка для верификации, добавляется после отправки команды.
        # Нужно будет скопировать ID сообщения и вставить вместо "...", после выполнения данных действий
        # необходимо перезапустить бота.
        self.bot.add_view(view=ButtonView(), message_id=...)


# Функция setup, которая добавляет класс Verify как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Verify(bot))
