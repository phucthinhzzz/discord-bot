import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import asyncio

# 1. Tải token từ file token.env
load_dotenv("token.env")

# 2. Thiết lập Intents
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        try:
            # Đồng bộ hóa tất cả slash commands
            synced = await self.tree.sync()
            print(f"✅ Đã sync {len(synced)} lệnh GLOBAL")
        except Exception as e:
            print(f"❌ Lỗi sync: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"🤖 Bot đã online: {bot.user}")

# --- Lệnh Prefix (!) ---
@bot.command()
async def hello(ctx):
    await ctx.send("Hello bro 😎")

# --- Lệnh Slash (/) cũ ---
@bot.tree.command(name="chui", description="Chửi nhẹ 🤡")
@app_commands.describe(user="Người bạn muốn chửi")
async def chui(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    chui_list = [
        f"{user.mention} nhìn là biết mày ngu 🤡",
        f"{user.mention} mày là đứa ăn mặn đái khai, ngu lâu dốt bền 🤣",
        f"{user.mention} địt mẹ mày ngu vậy 😭",
        f"{user.mention} tao không biết mày trai hay gái nhưng đọc được cái này thì mày là con chó 😭"
    ]
    await interaction.followup.send(random.choice(chui_list))

@bot.tree.command(name="khen", description="Khen người khác 😎")
@app_commands.describe(user="Người bạn muốn khen")
async def khen(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    khen_list = [
        f"{user.mention} đẹp trai nhất server 😎",
        f"{user.mention} là tiên nữ giáng thế 🧈"
    ]
    await interaction.followup.send(random.choice(khen_list))

# --- 3 LỆNH MỚI BỔ SUNG ---

@bot.tree.command(name="toxic_slap", description="Tát một cái kèm câu chửi ngẫu nhiên 👋🤡")
@app_commands.describe(user="Người bạn muốn tát")
async def toxic_slap(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    gif_list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3RrNmI2NjZqNnA5YWVjZWN1MzBvNTRiMzU4Ym0yamx0N2FpYWVpZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zy44YlR0ZUp3RjAybW9FL2dpcGh5LmdpZg"]
    slap_chui = [f"Mày chừa chưa hả {user.mention}? 👋🤡", f"Bớt mỏ hỗn lại nè {user.mention}! 👋😡"]
    await interaction.followup.send(f"{random.choice(slap_chui)}\n{random.choice(gif_list)}")

@bot.tree.command(name="rate", description="Chấm điểm ngẫu nhiên 📊")
@app_commands.describe(user="Người muốn chấm", type="Chấm điểm gì?")
async def rate(interaction: discord.Interaction, user: discord.Member, type: str):
    await interaction.response.defer()
    score = random.randint(1, 100)
    await interaction.followup.send(f"📊 **{type.upper()}** của {user.name} là: **{score}%**")

@bot.tree.command(name="avatar", description="Xem ảnh đại diện 📸")
@app_commands.describe(user="Người muốn xem")
async def avatar(interaction: discord.Interaction, user: discord.Member):
    url = user.avatar.url if user.avatar else user.default_avatar.url
    embed = discord.Embed(title=f"Avatar của {user.name}", color=discord.Color.blue())
    embed.set_image(url=url)
    await interaction.response.send_message(embed=embed)

# --- Khởi động Bot ---
if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ Không tìm thấy TOKEN trong file .env")
