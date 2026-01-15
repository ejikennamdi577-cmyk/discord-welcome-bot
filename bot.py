from keep_alive import keep_alive
import discord
from discord.ext import commands
import aiohttp
import io
from PIL import Image, ImageDraw

# Set up intents (permissions for the bot)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Your specific channel ID for welcome messages
WELCOME_CHANNEL_ID = 1446661159326584894

@bot.event
async def on_ready():
    print(f'{bot.user} is now online and ready!')
    print(f'Bot is in {len(bot.guilds)} server(s)')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    
    if channel:
        # Create the welcome message text
        welcome_message = (
            f"Hey {member.display_name} welcome to PARLAYS ENERGY 🏀🏈⚽ (let's eat) !\n"
            f"check out https://discord.com/channels/1446661158282068070/1446881476280057928 "
            f"and all channels in the server, feel the love and vibes"
        )
        
        # Download the background image
        background_url = "https://i.postimg.cc/wB0PDYCs/IMG-20251128-144143-389.jpg"
        avatar_url = str(member.display_avatar.url)
        
        async with aiohttp.ClientSession() as session:
            # Download background
            async with session.get(background_url) as resp:
                background_data = await resp.read()
            # Download avatar
            async with session.get(avatar_url) as resp:
                avatar_data = await resp.read()
        
        # Open images
        background = Image.open(io.BytesIO(background_data)).convert('RGBA')
        avatar = Image.open(io.BytesIO(avatar_data)).convert('RGBA')
        
        # Resize avatar to circular and place on background
        avatar_size = (120, 120)  # Size of the avatar circle
        avatar = avatar.resize(avatar_size, Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new('L', avatar_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=255)
        
        # Create a new image for the circular avatar
        circular_avatar = Image.new('RGBA', avatar_size)
        circular_avatar.paste(avatar, (0, 0))
        circular_avatar.putalpha(mask)
        
        # Calculate center position (adjust these numbers to move the avatar)
        bg_width, bg_height = background.size
        x = (bg_width - avatar_size[0]) // 2  # Center horizontally
        y = 180  # Adjust this number to move avatar up/down
        
        # Paste avatar onto background
        background.paste(circular_avatar, (x, y), circular_avatar)
        
        # Convert to RGB for JPEG
        background = background.convert('RGB')
        
        # Save to bytes
        final_image = io.BytesIO()
        background.save(final_image, format='JPEG', quality=95)
        final_image.seek(0)
        
        # Send message and image
        await channel.send(
            content=welcome_message,
            file=discord.File(final_image, 'welcome.jpg')
        )
        print(f'Welcomed {member.display_name} to the server!')
    else:
        print('Could not find welcome channel!')
keep_alive()
import os
bot.run(os.getenv('TOKEN'))