import discord
from discord import Intents
import aiohttp
import tensorflow as tf
import numpy as np
from PIL import Image, ImageSequence, ImageOps
import io
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Define intents
intents = Intents.default()
intents.messages = True
intents.guilds = True
# Enable this if your bot processes messages content and your bot is verified.
# intents.message_content = True

# Load your TensorFlow model
model = tf.saved_model.load('./')
classes = ["alastor", "not-alastor", "charlie"]

# Initialize Discord Client with intents
client = discord.Client(intents=intents)

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
                await message.channel.send(f'Image detected as: {class_detected}')
                if class_detected == "alastor":
                    await message.channel.send("Hello world")

    # Check for Giphy or Tenor links in the message content
    if 'giphy.com' in message.content or 'tenor.com' in message.content:
        class_detected = await process_gif(message.content)
        await message.channel.send(f'GIF detected as: {class_detected}')
        if class_detected == "alastor":
            await message.channel.send("Hello world")

# Use the bot token from the .env file to run the client
client.run(DISCORD_BOT_TOKEN)
