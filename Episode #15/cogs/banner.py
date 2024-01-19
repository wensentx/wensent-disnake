import io

from PIL import Image, ImageDraw, ImageFont
from disnake.ext import commands, tasks


class Banner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_banner.start()
        self.last = 0

    @tasks.loop(minutes=1)
    async def update_banner(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(...) # Укажите ID сервера
        with Image.open("Banner.png") as img:
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype("Gilroy-Medium.ttf", 130)
            total = len(guild.members)
            voice = len([m for m in guild.members if m.voice])
            if (total, voice) != self.last:
                x = 1292
                y = 311
                draw.text((x, y), str(voice), font=font)

                x = 1292
                y = 681
                draw.text((x, y), str(total), font=font)
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")
                img_bytes.seek(0)
                bytes = img_bytes.read()
                await guild.edit(banner=bytes)
                if (total, voice) != self.last:
                    self.last = (total, voice)


def setup(bot):
    bot.add_cog(Banner(bot))
