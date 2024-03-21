import discord
from discord import Intents
from discord import app_commands
import aiohttp
import tensorflow as tf
import numpy as np
from PIL import Image, ImageSequence, ImageOps
import io
from dotenv import load_dotenv
import os

from scoreboard import ScoreboardDB

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')

# Define intents
intents = Intents.default()
intents.messages = True
intents.guilds = True
# Enable this if your bot processes messages content and your bot is verified.
intents.message_content = True

# Load your TensorFlow model
model = tf.saved_model.load('./AlastorIdentifier')
classes = ["alastor", "not-alastor", "charlie"]

# Initialize Discord Client with intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Initialize the database for the scoreboard
scoreboard_db = ScoreboardDB()

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

def classify_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((300, 300 * img.size[1] // img.size[0]), Image.Resampling.LANCZOS)
    inp_numpy = np.array(img)[None]
    inp = tf.constant(inp_numpy, dtype='float32')
    class_scores = model(inp)[0].numpy()
    return classes[class_scores.argmax()]

async def process_gif(url):
    # Download the GIF
    gif_bytes = await download_image(url)
    gif = Image.open(io.BytesIO(gif_bytes))

    # Attempt to use the first frame of the GIF
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        break  # We only use the first frame

    # Convert PIL image to bytes
    buf = io.BytesIO()
    frame.save(buf, format='PNG')
    image_bytes = buf.getvalue()

    return classify_image(image_bytes)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=DISCORD_GUILD_ID))
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check for attachments in the message
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['jpg', 'jpeg', 'png', 'gif']):
                image_bytes = await download_image(attachment.url)
                class_detected = classify_image(image_bytes)
                if class_detected == "alastor":
                    await on_alastor_send(message)

    # Check for Giphy or Tenor links in the message content
    if 'giphy.com' in message.content or 'tenor.com' in message.content:
        class_detected = await process_gif(message.content + '.gif')
        if class_detected == "alastor":
            await on_alastor_send(message)


# Reward the user with a point if they send an alastor
async def on_alastor_send(message):
    await message.reply("You found Alastor! You get a point!")
    scoreboard_db.increment_score(message.author.id)


# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@tree.command(
    name="alastors",
    description="See who is the best person in this discord",
    guild=discord.Object(id=DISCORD_GUILD_ID)
)
async def first_command(interaction):
    leaderboard = scoreboard_db.get_leaderboard()
    embed = discord.Embed(title="Scoreboard", description="Top scores!", color=discord.Color.blue())
    for idx, (user_id, score) in enumerate(leaderboard, start=1):
        user = await client.fetch_user(user_id)
        embed.add_field(name=f"{idx}. {user.display_name}", value=f"Score: {score}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# Use the bot token from the .env file to run the client
client.run(DISCORD_BOT_TOKEN)
