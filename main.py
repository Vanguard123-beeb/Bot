import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# ──────────────────────────────────────────────
#  🌐  Keep-alive web server (prevents sleep)
# ──────────────────────────────────────────────
app = Flask(__name__)

@app.route("/")
def home():
    return "⚔️ Vanguard Hub — Online"

Thread(target=lambda: app.run(host="0.0.0.0", port=10000), daemon=True).start()

# ──────────────────────────────────────────────
#  🤖  Bot setup
# ──────────────────────────────────────────────
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ──────────────────────────────────────────────
#  📦  Script registry
# ──────────────────────────────────────────────
SCRIPTS: dict[str, dict] = {
    "brainrot_heroes": {
        "label":       "Brainrot Heroes",
        "version":     "v2.0.0",
        "emoji":       "🏹",
        "description": "Vanguard Hub • Auto-farm & utilities",
        "code": (
            "loadstring(game:HttpGet("
            "'https://api.jnkie.com/api/v1/luascripts/public/"
            "436af5e1d82be2ee4aab5c9482124244d2a01a894933a45fe599e5de76fadc10"
            "/download'))()"
        ),
    },
    "luckyblock_farm": {
        "label":       "Be a Lucky Block",
        "version":     "v1.0.0",
        "emoji":       "🚜",
        "description": "Vanguard Hub • Lucky block farmer",
        "code": (
            "loadstring(game:HttpGet("
            "'https://api.jnkie.com/api/v1/luascripts/public/"
            "2dc0f23ac42daa51fd8239d28e46f479966f9f5749216f9a03c3ad170319f224"
            "/download'))()"
        ),
    },
}

# ──────────────────────────────────────────────
#  🎛️  UI Components
# ──────────────────────────────────────────────
class ScriptSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=f"{info['label']}  {info['version']}",
                description=info["description"],
                emoji=info["emoji"],
                value=key,
            )
            for key, info in SCRIPTS.items()
        ]
        super().__init__(
            placeholder="▸  Choose a script...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        key  = self.values[0]
        info = SCRIPTS[key]

        embed = discord.Embed(
            title=f"{info['emoji']}  {info['label']}  —  {info['version']}",
            description=f"```lua\n{info['code']}\n```",
            color=0x5865F2,
        )
        embed.set_footer(text="Vanguard Hub  •  Copy & paste into your executor")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ScriptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ScriptSelect())


# ──────────────────────────────────────────────
#  🚀  Events & commands
# ──────────────────────────────────────────────
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Vanguard Hub  ⚔️",
        )
    )
    print(f"[✓] Logged in as {bot.user}  (ID: {bot.user.id})")
    print("─" * 40)


@bot.tree.command(name="script", description="Browse & grab Vanguard Hub scripts")
async def script_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚔️  Vanguard Hub  —  Script Menu",
        description=(
            "Select a script from the dropdown below.\n"
            "The code will be sent **only to you**.\n\n"
            "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
        ),
        color=0x5865F2,
    )
    embed.set_footer(text="Vanguard Hub  •  Use at your own risk")
    await interaction.response.send_message(embed=embed, view=ScriptView())


# ──────────────────────────────────────────────
#  🔌  Run
# ──────────────────────────────────────────────
bot.run(TOKEN)
