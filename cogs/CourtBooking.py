import asyncio

from discord.ext import commands


# Helper function for threading multiple book court calls.
async def run_subprocess(month, day, time, am_pm, token, ctx) -> None:
    command = ["python", 'cogs/CourtBookingFiles/BookCourt.py', month, day, time, am_pm, str(1), token]

    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=False
        )
        await ctx.channel.send(f'Scheduled to book on {month}/{day} at {time}{am_pm}.')
        while True:
            output = await process.stdout.readline()
            if not output:
                break
            print(output.decode().strip())
        await ctx.channel.send(f'{ctx.author.mention}, Booking Successful!')
        # !TODO: check if the court is actually booked before sending the booking successful message.
    except Exception as e:
        await ctx.channel.send(f'Error: {e}')


# Helper function to check every parameter is present and in correct format.
async def check_parameters(month, day, time, am_pm, ctx) -> bool:
    if not (month.isdigit() and day.isdigit() and time.isdigit()):
        await ctx.channel.send("Month, day, and hour should be numbers.")
        return False

    if am_pm not in ["AM", "PM"]:
        await ctx.channel.send("AM or PM must be either AM or PM.")
        return False

    return True


class BookCourt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def book(self, ctx) -> None:
        parameter = ctx.message.content[6:].split(" ")

        month = parameter[0]
        day = parameter[1]
        time = parameter[2]
        am_pm = parameter[3]
        token = parameter[4]

        if await check_parameters(month, day, time, am_pm, ctx):
            await run_subprocess(month, day, time, am_pm, token, ctx)


async def setup(client):
    await client.add_cog(BookCourt(client))
