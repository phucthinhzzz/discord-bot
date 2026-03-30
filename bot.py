import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random

load_dotenv("token.env")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()

class MyBot(commands.Bot):
    async def setup_hook(self):
        # Sync global command (toàn bộ server)
        try:
            await self.tree.sync()
            print("✅ Đã sync slash command GLOBAL")
        except Exception as e:
            print("❌ Lỗi sync:", e)

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot đã online: {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello bro 😎")

@bot.tree.command(name="chui", description="Chửi thấy mẹ nó 🤡")
@app_commands.describe(user="Người bạn muốn chửi")
async def chui(interaction: discord.Interaction, user: discord.Member):
    chui_list = [
        f"{user.mention} nhìn là biết mày ngu rồi 🤡",
        f"{user.mention} mày là đứa ăn mặn đái khai , ngu lâu dốt bền  🤣",
        f"{user.mention} địt mẹ mày ngu vậy ; 😭"
    ]
    await interaction.response.send_message(random.choice(chui_list))
async def setup_hook(self):
    try:
        # Sync global nhưng giữ nguyên command hệ thống
        synced = await self.tree.sync()
        print(f"✅ Đã sync {len(synced)} lệnh GLOBAL")
    except discord.HTTPException as e:
        print("❌ Lỗi sync:", e)
bot.run(TOKEN)
