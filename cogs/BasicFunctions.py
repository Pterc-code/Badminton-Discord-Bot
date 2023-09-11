# Imports
import discord
from discord.ext import commands, tasks


class BasicFunctions(commands.Cog):
    """
    Class to hold all basic events and commands
    """
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_command_error(self, ctx, errors) -> None:
        """
        Gives out an error when command is called without proper arguments
        """
        if isinstance(errors, commands.MissingRequiredArgument):
            await ctx.send("You're missing a required argument!")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        Prints in terminal indicating when the bot is online
        """
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Game("Badminton"))
        print("Bot is online.")

    # Commands
    @commands.command()
    async def ping(self, ctx) -> None:
        """
        Prints bot latency
        """
        await ctx.send(f"The ping is {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def clear(self, ctx, amount: int) -> None:
        """
        Deletes 'amount' of messages
        """
        await ctx.channel.purge(limit=amount)


# Setup cog for client
async def setup(client):
    await client.add_cog(BasicFunctions(client))
