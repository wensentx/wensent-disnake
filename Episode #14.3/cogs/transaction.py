import disnake
from disnake.ext import commands
from utils.databases import UsersDataBase


class Buttons(disnake.ui.View):
    def __init__(self, embeds, interaction):
        super().__init__(timeout=60)
        self.embeds = embeds
        self.interaction = interaction
        self.offset = 0

        for emb in self.embeds:
            emb.set_footer(text=f'Страница {self.embeds.index(emb) + 1}/{len(self.embeds)}')

    async def update_button(self):
        offset = self.offset
        is_first_page = offset == 0
        is_last_page = offset == len(self.embeds) - 1

        self.back.disabled = is_first_page
        self.forward.disabled = is_last_page

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if self.interaction.author.id != interaction.user.id:
            embed = disnake.Embed(color=0xff0000).set_author(name="[Ошибка] История транзакций")
            embed.description = (
                f"{interaction.author.mention}, Вы **не** можете использовать эту кнопку, "
                f"так как она предназначена для пользователя {self.interaction.author.mention}!")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        return True

    @disnake.ui.button(label='Назад', style=disnake.ButtonStyle.grey)
    async def back(self, _, interaction: disnake.MessageInteraction):
        self.offset -= 1
        await self.update_button()
        await interaction.response.edit_message(embed=self.embeds[self.offset], view=self)

    @disnake.ui.button(label='Вперед', style=disnake.ButtonStyle.grey)
    async def forward(self, _, interaction: disnake.MessageInteraction):
        self.offset += 1
        await self.update_button()
        await interaction.response.edit_message(embed=self.embeds[self.offset], view=self)

    @disnake.ui.button(label='Закрыть', style=disnake.ButtonStyle.red)
    async def close(self, _, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        await interaction.delete_original_response()


class Transactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_users = UsersDataBase()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.db_users.create_table()

    @commands.slash_command(name='transaction', description="Посмотреть транзакции")
    async def transaction(self, interaction: disnake.CommandInteraction):
        embeds = await self.db_users.get_embeds(interaction)
        if len(embeds) == 0:
            return await interaction.response.send_message(
                f'{interaction.author.mention}, у вас нет **транзакций**. '
                f'Совершите **транзакцию**, чтобы она отобразилась здесь.',
                ephemeral=True)
        view = Buttons(embeds, interaction)
        await view.update_button()
        await interaction.response.send_message(embed=embeds[0], view=view, ephemeral=True)

    # Сделаем фейковые методы для добавления транзакций.
    # Их можно удалить, после внедрения данного кода, в вашего бота
    @commands.slash_command(name='add_transaction', description="Добавить транзакцию")
    async def add_transaction(self, interaction: disnake.CommandInteraction):
        await self.db_users.add_transaction(
            interaction.author.id,
            100,
            "Пополнение баланса"
        )
        await interaction.response.send_message("Транзакция добавлена!", ephemeral=True)

    @commands.slash_command(name='add_transaction2', description="Добавить транзакцию")
    async def add_transaction2(self, interaction: disnake.CommandInteraction):
        await self.db_users.add_transaction(interaction.author.id, -100, "Покупка роли")
        await interaction.response.send_message("Транзакция добавлена!", ephemeral=True)


def setup(bot):
    bot.add_cog(Transactions(bot))
