import discord
from discord import app_commands
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 🌐 Web server (กัน Render sleep)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run_web).start()

# 🔑 Token จาก environment
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class ScriptSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Brainrot Heroes", description="สคริปต์หลัก", emoji="🏹", value="brainrot_heroes"),
            discord.SelectOption(label="Be a lucky block", description="สคริปต์ฟาร์ม", emoji="🚜", value="luckyblock_farm"),
        ]
        super().__init__(placeholder="เลือกสคริปต์...", options=options)

    async def callback(self, interaction: discord.Interaction):
        scripts = {
            "brainrot_heroes": "loadstring(game:HttpGet('https://api.jnkie.com/api/v1/luascripts/public/436af5e1d82be2ee4aab5c9482124244d2a01a894933a45fe599e5de76fadc10/download'))()",
            "luckyblock_farm": "loadstring(game:HttpGet('https://api.jnkie.com/api/v1/luascripts/public/2dc0f23ac42daa51fd8239d28e46f479966f9f5749216f9a03c3ad170319f224/download'))()",
        }

        selected_name = [opt.label for opt in self.options if opt.value == self.values[0]][0]
        script_code = scripts.get(self.values[0], "ไม่พบสคริปต์")

        embed = discord.Embed(
            title=f"🚀 {selected_name}",
            description=f"```lua\n{script_code}\n```",
            color=0x2f3136
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

class ScriptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ScriptSelect())

@bot.event
async def on_ready():
    print(f'✅ {bot.user} ออนไลน์แล้ว')
    await bot.tree.sync()

@bot.tree.command(name="script")
async def script(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛡️ Vanguard Hub Script Menu",
        description="เลือกสคริปต์ด้านล่าง",
        color=0x2f3136
    )
    await interaction.response.send_message(embed=embed, view=ScriptView())

bot.run(TOKEN)
