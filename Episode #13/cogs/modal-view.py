# Импортируем необходимые модули из библиотеки disnake.
import disnake
from disnake.ext import commands


# Определяем класс "RecruitementModal", который наследуется от disnake.ui.Modal.
class RecruitementModal(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg  # arg - это аргумент, который передается в конструкторе класса RecruitementSelect

        # Создаем компоненты ввода текста (TextInput) для имени и возраста.
        components = [
            disnake.ui.TextInput(label="Ваше имя", placeholder="Введите ваше имя", custom_id="name"),
            disnake.ui.TextInput(label="Ваш возраст", placeholder="Введите ваш возраст", custom_id="age")
        ]

        # Определяем заголовок модального окна в зависимости от аргумента "arg".
        if self.arg == "moderator":
            title = "Набор на должность модератора"
        else:
            title = "Набор на должность ведущего"

        super().__init__(title=title, components=components, custom_id="recruitementModal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values["name"]
        age = interaction.text_values["age"]

        # Создаем и отправляем ответное сообщение с подтверждением заявки.
        embed = disnake.Embed(color=0x2F3136, title="Заявка отправлена!")
        embed.description = f"{interaction.author.mention}, Благодарим вас за **заявку**! " \
                            f"Если вы нам **подходите**, администрация **свяжется** с вами в ближайшее время."
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Получаем канал, куда будут отправляться заявки (необходимо указать ID канала).
        channel = interaction.guild.get_channel(...)  # Вставить ID канала куда будут отправляться заявки
        await channel.send(f"Заявка на должность {self.arg} от {name} {interaction.author.mention} ({age} лет)")


# Определяем класс "RecruitementSelect", который наследуется от disnake.ui.Select.
class RecruitementSelect(disnake.ui.Select):
    def __init__(self):
        # Создаем опции для выбора ролей.
        options = [
            disnake.SelectOption(label="Модератор", value="moderator", description="Модератор сервера"),
            disnake.SelectOption(label="Ведущий", value="eventsmod", description="Ведущий мероприятий"),
        ]

        super().__init__(
            placeholder="Выбери желаемую роль", options=options, min_values=0, max_values=1, custom_id="recruitement"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(RecruitementModal(interaction.values[0]))


# Определяем класс "Recruitement", который является расширением (Cog) для бота.
class Recruitement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    # Создаем команду "recruit", которая будет выводить сообщение с выбором ролей.
    @commands.command()
    async def recruit(self, ctx):
        view = disnake.ui.View()
        view.add_item(RecruitementSelect())

        # Отправляем сообщение с выбором ролей и предложением подать заявку.
        await ctx.send('Выбери желаемую роль', view=view)

    # Создаем слушателя события "on_ready", который добавляет персистентное меню выбора ролей.
    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitementSelect())

        # Message ID сообщения, где будет меню выбора ролей, добавляется после отправки команды.
        # Нужно будет скопировать ID сообщения и вставить вместо "...", после выполнения данных действий
        # необходимо перезапустить бота.
        self.bot.add_view(view, message_id=...)


# Функция setup, которая добавляет класс Recruitement как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(Recruitement(bot))
