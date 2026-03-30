import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import asyncio

# 1. Tải token từ file môi trường
# Theo cấu hình của bạn, file này tên là 'token.env'
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
            # Đồng bộ hóa tất cả slash commands lên hệ thống Discord
            synced = await self.tree.sync()
            print(f"✅ Đã sync {len(synced)} lệnh thành công!")
        except Exception as e:
            print(f"❌ Lỗi sync lệnh: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"🤖 Bot {bot.user} đã sẵn sàng!")

# --- CÁC LỆNH SLASH (/) ---

@bot.tree.command(name="chui", description="Chửi nhẹ một ai đó 🤡")
@app_commands.describe(user="Người bạn muốn chửi")
async def chui(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer() # Tránh lỗi timeout 3s
    chui_list = [
        f"{user.mention} nhìn là biết mày ngu 🤡",
        f"{user.mention} mày là đứa ăn mặn đái khai, ngu lâu dốt bền 🤣",
        f"{user.mention} địt mẹ mày ngu vậy 😭",
        f"{user.mention} tao không biết mày trai hay gái nhưng đọc được cái này thì mày là con chó 😭"
    ]
    await interaction.followup.send(random.choice(chui_list))

@bot.tree.command(name="khen", description="Khen ngợi một người 😎")
@app_commands.describe(user="Người bạn muốn khen")
async def khen(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    khen_list = [
        f"{user.mention} đẹp trai nhất server 😎",
        f"{user.mention} là tiên nữ giáng thế 🧈"
    ]
    await interaction.followup.send(random.choice(khen_list))

@bot.tree.command(name="toxic_slap", description="Tát một cái kèm câu chửi ngẫu nhiên 👋🤡")
@app_commands.describe(user="Người bạn muốn tát")
async def toxic_slap(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3RrNmI2NjZqNnA5YWVjZWN1MzBvNTRiMzU4Ym0yamx0N2FpYWVpZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zy44YlR0ZUp3RjAybW9FL2dpcGh5LmdpZg"
    cau_chui = [f"Chừa chưa hả {user.mention}? 👋🤡", f"Bớt mỏ hỗn lại nè {user.mention}! 👋😡"]
    await interaction.followup.send(f"{random.choice(cau_chui)}\n{gif_url}")

@bot.tree.command(name="rate", description="Chấm điểm ngẫu nhiên 📊")
@app_commands.describe(user="Người muốn chấm", type="Nội dung muốn chấm (VD: độ ngu, độ đẹp)")
async def rate(interaction: discord.Interaction, user: discord.Member, type: str):
    await interaction.response.defer()
    score = random.randint(1, 100)
    await interaction.followup.send(f"📊 **{type.upper()}** của {user.name} là: **{score}%**")

@bot.tree.command(name="avatar", description="Xem ảnh đại diện kích thước lớn 📸")
@app_commands.describe(user="Người bạn muốn xem ảnh")
async def avatar(interaction: discord.Interaction, user: discord.Member):
    # Lấy URL avatar, nếu không có thì lấy ảnh mặc định
    url = user.avatar.url if user.avatar else user.default_avatar.url
    embed = discord.Embed(title=f"Avatar của {user.name}", color=discord.Color.blue())
    embed.set_image(url=url)
    await interaction.response.send_message(embed=embed)

# --- KHỐI CHẠY BOT ---
if __name__ == "__main__":
    # Lấy token từ biến môi trường trong file token.env
    token_value = os.getenv("TOKEN")
    if token_value:
        bot.run(token_value)
    else:
        print("❌ LỖI: Không tìm thấy 'TOKEN' trong file token.env!")
