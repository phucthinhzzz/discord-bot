import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import asyncio # Thêm thư viện để dùng asyncio.sleep()

# Load token từ file token.env như bạn đã đặt tên
# Đảm bảo trong file token.env có dòng: TOKEN=your_real_token_here
load_dotenv("token.env")

# Khai báo Intents (Quyền hạn)
# Đảm bảo bạn đã bật 'Message Content Intent' và 'Server Members Intent' trên Discord Developer Portal
intents = discord.Intents.default()
intents.message_content = True  # Cần cho lệnh prefix '!'
intents.members = True          # Bắt buộc để nhận diện discord.Member trong Slash Commands

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        try:
            # Sync global commands (toàn bộ server)
            await self.tree.sync()
            print("✅ Đã sync slash command GLOBAL")
        except Exception as e:
            print(f"❌ Lỗi sync: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"🤖 Bot đã online: {bot.user}")
    print("---------------------------------")

# --- Lệnh Prefix cũ của bạn ---

@bot.command()
async def hello(ctx):
    await ctx.send("Hello bro 😎")

# --- Nhóm lệnh Slash Command Tương tác cũ ---

@bot.tree.command(name="chui", description="Chửi nhẹ 🤡")
@app_commands.describe(user="Người bạn muốn chửi")
async def chui(interaction: discord.Interaction, user: discord.Member):
    # Dùng defer() để tránh timeout 3s
    await interaction.response.defer()
    
    chui_list = [
        f"{user.mention} nhìn là biết mày ngu 🤡",
        f"{user.mention} mày là đứa ăn mặn đái khai, ngu lâu dốt bền 🤣",
        f"{user.mention} địt mẹ mày ngu vậy 😭",
        f"{user.mention} đọc được cái này thì mày là con chó 😭"
    ]
    # Dùng followup.send để gửi tin nhắn sau khi defer
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

# --- BỔ SUNG: 3 LỆNH NÂNG CẤP MỚI ---

@bot.tree.command(name="toxic_slap", description="Tát một cái kèm câu chửi ngẫu nhiên 👋🤡")
@app_commands.describe(user="Người bạn muốn tát")
async def toxic_slap(interaction: discord.Interaction, user: discord.Member):
    # 1. Xin thêm thời gian (tránh lỗi 3 giây)
    await interaction.response.defer()
    
    # 2. Danh sách ảnh GIF tát (bạn có thể thay link khác nếu muốn)
    gif_list = [
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3RrNmI2NjZqNnA5YWVjZWN1MzBvNTRiMzU4Ym0yamx0N2FpYWVpZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zy44YlR0ZUp3RjAybW9FL2dpcGh5LmdpZg", # Tát vui
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3RrNmI2NjZqNnA5YWVjZWN1MzBvNTRiMzU4Ym0yamx0N2FpYWVpZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zy44YlR0ZUp3RjAybW9FL2dpcGh5LmdpZg", # Tát mạnh (có thể đổi link)
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3RrNmI2NjZqNnA5YWVjZWN1MzBvNTRiMzU4Ym0yamx0N2FpYWVpZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zy44YlR0ZUp3RjAybW9FL2dpcGh5LmdpZg"  # Tát liên hoàn (có thể đổi link)
    ]
    
    # 3. Danh sách câu chửi khi tát
    slap_chui_list = [
        f"Mày chừa chưa hả {user.mention}? Đồ ngu! 👋🤡",
        f"Một vả cho tỉnh ngộ nè {user.mention}, bớt mỏ hỗn lại! 🤣",
        f"{user.mention} cái tát này là dành cho sự ngu lâu dốt bền của mày! 👋😭",
        f"Tao tát cho mày tỉnh cái đầu chó của mày ra {user.mention}! 👋😡"
    ]
    
    # 4. Giả lập xử lý (ví dụ: chọn GIF) mất 1 giây
    await asyncio.sleep(1)
    
    # 5. Gửi tin nhắn kết hợp cả câu chửi và ảnh GIF
    message = f"{random.choice(slap_chui_list)}\n\n{random.choice(gif_list)}"
    await interaction.followup.send(message)

@bot.tree.command(name="rate", description="Chấm điểm ngẫu nhiên từ 1-100% 📊")
@app_commands.describe(user="Người bạn muốn chấm điểm", type="Bạn muốn chấm điểm gì? (Ví dụ: độ ngu, độ đẹp trai)")
async def rate(interaction: discord.Interaction, user: discord.Member, type: str):
    await interaction.response.defer()
    
    # 1. Tạo điểm ngẫu nhiên
    score = random.randint(1, 100)
    
    # 2. Tạo câu nhận xét dựa trên điểm số
    comment = ""
    if score < 20:
        comment = "Thôi xong, ca này bot cạn lời... 💀"
    elif score < 50:
        comment = "Cần cố gắng nhiều hơn nữa bro ơi. 😕"
    elif score < 80:
        comment = "Khá khen, cũng ra gì và này nọ đấy! 😎"
    else:
        comment = "Quá đỉnh! Không còn gì để chê! 🔥🧈"
        
    # 3. Giả lập xử lý mất 1 giây
    await asyncio.sleep(1)
    
    # 4. Gửi kết quả
    result = f"📊 **Bảng xếp hạng {type.upper()} của {user.name}:**\n\n> Điểm số: **{score}%**\n> Nhận xét: {comment}"
    await interaction.followup.send(result)

@bot.tree.command(name="avatar", description="Xem ảnh đại diện kích thước lớn 📸")
@app_commands.describe(user="Người bạn muốn xem ảnh")
async def avatar(interaction: discord.Interaction, user: discord.Member):
    # Lệnh này xử lý rất nhanh, không cần defer()
    
    # 1. Kiểm tra xem người dùng có avatar không
    if user.avatar:
        avatar_url = user.avatar.url
    else:
        # Nếu không có, lấy ảnh mặc định của Discord
        avatar_url = user.default_avatar.url
        
    # 2. Tạo Embed để hiển thị ảnh đẹp hơn
    embed = discord.Embed(
        title=f"Ảnh đại diện của {user.name}",
        description=f"Click vào đây để [tải ảnh xuống]({avatar_url})",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)
    
    # 3. Gửi Embed
    await interaction.response.send_message(embed=embed)

# --- Khối chạy Bot chuẩn ---

if __name__ == "__main__":
    # 1. Lấy token từ biến môi trường
    token = os.getenv("TOKEN")
    
    if token:
        # 2. Chạy bot
        try:
            bot.run(token)
        except Exception as e:
            print(f"❌ Lỗi khi chạy bot: {e}")
            print("Vui lòng kiểm tra lại TOKEN và quyền hạn Intents trên Developer Portal.")
    else:
        print("❌ Không tìm thấy TOKEN trong file token.env.")
        print("Hãy chắc chắn bạn đã tạo file 'token.env' cùng thư mục với 'bot.py' và ghi: TOKEN=your_actual_token")
