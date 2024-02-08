from datetime import datetime

from cogs.staticVariables.staticVariables import *

import requests
import schedule
from discord.ext import commands, tasks
from pyquery import PyQuery

application_cookie = []


def update_application_cookie():
    global application_cookie
    try:
        x = requests.get(
            'https://recreation.utoronto.ca/booking/33215bab-05b9-41de-be04-c9ae496d5609/slots/4c99c8bd-f117-4603-bba6-c8e2e9614799/2024/%s')
        updated_cookie = x.cookies.get_dict().get('.AspNet.ApplicationCookie')
        application_cookie = application_cookie if updated_cookie is None else updated_cookie
    except Exception as e:
            print(f"An error occurred: {e}")


schedule.every(1).minutes.do(update_application_cookie)


def get_court_data(booking_date):
    request1 = requests.get(
        'https://recreation.utoronto.ca/booking/%s/slots/%s/2024/%s' % (court1_id, court1_fid, booking_date),
        headers={"accept": "*/*",
                 "accept-encoding": "gzip, deflate, br",
                 "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,und;q=0.4",
                 "referer": "https://recreation.utoronto.ca/booking/%s" % court1_id,
                 "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": "'windows'",
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                 "x-requested-with": "XMLHttpRequest",
                 "cookie": ".AspNet.ApplicationCookie=%s" % application_cookie,
                 }).text

    request2 = requests.get(
        'https://recreation.utoronto.ca/booking/%s/slots/%s/2024/%s' % (court2_id, court2_fid, booking_date),
        headers={"accept": "*/*",
                 "accept-encoding": "gzip, deflate, br",
                 "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,und;q=0.4",
                 "referer": "https://recreation.utoronto.ca/booking/%s" % court2_id,
                 "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": "'windows'",
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                 "x-requested-with": "XMLHttpRequest",
                 "cookie": ".AspNet.ApplicationCookie=%s" % application_cookie,
                 }).text

    request3 = requests.get(
        'https://recreation.utoronto.ca/booking/%s/slots/%s/2024/%s' % (court3_id, court3_fid, booking_date),
        headers={"accept": "*/*",
                 "accept-encoding": "gzip, deflate, br",
                 "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,und;q=0.4",
                 "referer": "https://recreation.utoronto.ca/booking/%s" % court3_id,
                 "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": "'windows'",
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                 "x-requested-with": "XMLHttpRequest",
                 "cookie": ".AspNet.ApplicationCookie=%s" % application_cookie,
                 }).text

    return request1, request2, request3


def get_court_hours(court_data, day, month):
    pm_data = []

    for i in range(len(court_data)):
        pq = PyQuery(court_data[i])
        data = pq('div.booking-slot-item').text()
        data = data.strip().split('\n')[1:]
        # Get the current time
        current_time = datetime.now().replace(minute=0, day=int(day))

        # Iterate through the lines and extract time and availability for PM slots
        for j in range(0, len(data), 2):
            if "PM" in data[j]:
                time_info = data[j].split(' ')[2:]
                time_str = "".join(time_info)
                time = datetime.strptime(time_str, "%I:%M%p").replace(
                    year=current_time.year,
                    month=current_time.month,
                    day=int(day),
                    minute=0
                )

                if current_time < time:
                    pm_data.append((i + 1, data[j], data[j + 1], day, month))

    return pm_data


async def notify_user(pm_data, ctx):
    court = False
    for i in range(len(pm_data)):
        if "1 spot available" in pm_data[i][2]:
            court = True
            await ctx.channel.send(
                f'{ctx.author.mention} Court {pm_data[i][0]} on {pm_data[i][4]}/{pm_data[i][3]} at {pm_data[i][1]} is open for booking.')
    return court


class CourtNotification(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ctx = None
        self.month = None
        self.day = None
        self.booking_date = None

    @commands.command()
    async def notify(self, ctx) -> None:
        await ctx.channel.purge(limit=1)

        global application_cookie
        self.ctx = ctx
        parameter = self.ctx.message.content[7:].split(" ")
        self.month = parameter[1]
        self.day = parameter[2]
        self.booking_date = '%s/%s' % (self.month, self.day)
        application_cookie = parameter[3]

        await ctx.channel.send(f'{ctx.author.mention} is looking for courts on {self.month}/{self.day}.')
        await self.notification_task.start()

    @tasks.loop(seconds=30)
    async def notification_task(self):
        try:
            # Setting variables
            global application_cookie

            # Getting court information
            court_data = get_court_data(self.booking_date)
            court_hours = get_court_hours(court_data, self.day, self.month)
            if not await notify_user(court_hours, self.ctx):
                pass
            else:
                self.notification_task.stop()
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(client):
    await client.add_cog(CourtNotification(client))
