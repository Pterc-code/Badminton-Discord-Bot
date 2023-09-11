# Imports
import asyncio
import os

from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()

# sets the command prefix to !
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Bot token
TOKEN = os.environ.get('BOT_TOKEN')


# Basic Commands
@client.command()
async def load(ctx, extension) -> None:
    """
    Loads the cog with name: extension
    """
    await client.load_extension(f"cogs.{extension}")
    await ctx.send('Loaded ' + extension)


@client.command()
async def unload(ctx, extension) -> None:
    """
    Unloads the cog with name: extension
    """
    await client.unload_extension(f"cogs.{extension}")
    await ctx.send('Unloaded ' + extension)


@client.command()
async def reload(ctx, extension) -> None:
    """
    Reloads the cogs for ease of access
    """
    await client.unload_extension(f"cogs.{extension}")
    await client.load_extension(f"cogs.{extension}")
    await ctx.send('Reloaded ' + extension)


# Load Cogs
async def main() -> None:
    async with client:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.start(TOKEN)


asyncio.run(main())
