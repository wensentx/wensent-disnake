from disnake.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, interaction):
        await interaction.response.send_message("Pong!")


def setup(bot):
    bot.add_cog(Ping(bot))
