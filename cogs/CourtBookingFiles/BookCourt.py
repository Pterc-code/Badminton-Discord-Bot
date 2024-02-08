import sys

global application_cookie
month, day, book_hours, am_or_pms, book_person, application_cookie = sys.argv[1:]
book_hours = [int(hour) for hour in book_hours.strip("[").strip("]").split(",")]
am_or_pms = am_or_pms.strip("[").strip("]").split(",")
for s in am_or_pms:
    assert s in ["AM", "PM"]
assert len(book_hours) == len(am_or_pms)
assert book_person in ['1', '2', '3']
year = '2024'
time_12to24 = {(hour, AMPM): hour + (0 if AMPM == "AM" or hour == 12 else 12) for hour in range(1, 13) for AMPM in
               ["AM", "PM"]}
booking_date = '%s/%s' % (month, day)
court1_id = '33215bab-05b9-41de-be04-c9ae496d5609'
court1_fid = '4c99c8bd-f117-4603-bba6-c8e2e9614799'
court2_id = '33215bab-05b9-41de-be04-c9ae496d5609'
court2_fid = '9f64ef55-8eba-4a7a-99d1-1c94d7478b1c'
court3_id = '33215bab-05b9-41de-be04-c9ae496d5609'
court3_fid = '59d31228-780c-49bc-8454-d6cbd093277c'
import requests
import schedule
import time
from datetime import datetime


def update_application_cookie():
    print("updating cookie")
    global application_cookie
    x = requests.get(
        'https://recreation.utoronto.ca/booking/33215bab-05b9-41de-be04-c9ae496d5609/slots/4c99c8bd-f117-4603-bba6-c8e2e9614799/2024/%s' % booking_date,
        headers={"accept": "*/*",
                 "accept-encoding": "gzip, deflate, br",
                 "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,und;q=0.4",
                 "referer": "https://recreation.utoronto.ca/booking/af97abfd-f094-49c4-8a17-9330879ed6cc",
                 "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": "'windows'",
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                 "x-requested-with": "XMLHttpRequest",
                 "cookie": ".AspNet.ApplicationCookie=%s" % application_cookie,
                 })
    updated_cookie = x.cookies.get_dict().get('.AspNet.ApplicationCookie')
    print(updated_cookie)
    application_cookie = application_cookie if updated_cookie is None else updated_cookie


# Used for pulling right before the hour, extract id, and book
def extract_keyword(string, keyword):
    # split the string by the keyword
    split = string.split(keyword)
    # assert len(split) > 1, "keyword not found"
    # loop through each split and extract the value
    # ignore the first split since that was before the first keyword
    values = []
    for i in range(1, len(split)):
        # find the value in the quotes
        assert split[i][:2] == '="', "expected the value to start with quotes"
        values.append(split[i].split('"')[1])
    return values


def get_timeslot_string(string: str, hour: int, AMPM: str):
    AMPM = AMPM.upper()
    assert AMPM in ["AM", "PM"]
    max_button_len = len("12:15 - 12:55 PM")  # maximum button length as a string
    # split the string into timeslots
    splits = string.split("</strong></p>")
    # get the timeslot as a string which we know will appear uniquely for this button
    hour_str = " %d:" % (hour)
    # find the timeslot
    for split in splits:
        # get the string from the button
        button_str = split[-max_button_len:]
        # determine if this button is the right timeslot
        if hour_str in button_str and AMPM in button_str:
            # then just return this whole split
            return split
    # if we end up here then there is no timeslot, this could be caused by authentication is stripping out of sync and so should kill the program since no valid authentication is available at this point.
    print("Warning: timeslot %d%s not found on page." % (hour, AMPM))
    # print(string)
    assert False


def book_court():
    data_apt_id1 = []
    data_apt_id2 = []
    data_apt_id3 = []
    data_timeslot_id1 = []
    data_timeslot_id2 = []
    data_timeslot_id3 = []
    time.sleep(0.05)
    t0 = time.time()
    while len(data_apt_id2) == 0 and time.time() - t0 < 500:

        # Dumb way to book all three courts -- but it worked anyways
        request1 = requests.get('https://recreation.utoronto.ca/booking/%s/slots/%s/2024/%s' % (court1_id, court1_fid, booking_date),
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
                                  })

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
                     })

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
                     })

        timeslot_string1 = get_timeslot_string(request1.text, hour=book_hour, AMPM=am_or_pm)
        data_apt_id1 = extract_keyword(timeslot_string1, "data-apt-id")
        data_timeslot_id1 = extract_keyword(timeslot_string1, "data-timeslot-id")

        timeslot_string2 = get_timeslot_string(request2.text, hour=book_hour, AMPM=am_or_pm)
        data_apt_id2 = extract_keyword(timeslot_string2, "data-apt-id")
        data_timeslot_id2 = extract_keyword(timeslot_string2, "data-timeslot-id")

        timeslot_string3 = get_timeslot_string(request3.text, hour=book_hour, AMPM=am_or_pm)
        data_apt_id3 = extract_keyword(timeslot_string3, "data-apt-id")
        data_timeslot_id3 = extract_keyword(timeslot_string3, "data-timeslot-id")

        # data_timeslotinstance_id = extract_keyword(timeslot_string, "data-timeslotinstance-id")
        if len(data_apt_id2) > 0:
            data1 = {
                "bId": court1_id,  # booking/court-id
                "fId": court1_fid,  # No change
                "aId": data_apt_id1[0],
                "tsId": data_timeslot_id1[0],
                "tsiId": "00000000-0000-0000-0000-000000000000",  # Sometimes m
                "y": year,
                "m": month,
                "d": day,
                "t": "",
                "v": "0"}

            data2 = {
                "bId": court2_id,  # booking/court-id
                "fId": court2_fid,  # No change
                "aId": data_apt_id2[0],
                "tsId": data_timeslot_id2[0],
                "tsiId": "00000000-0000-0000-0000-000000000000",  # Sometimes m
                "y": year,
                "m": month,
                "d": day,
                "t": "",
                "v": "0"}

            data3 = {
                "bId": court3_id,  # booking/court-id
                "fId": court3_fid,  # No change
                "aId": data_apt_id3[0],
                "tsId": data_timeslot_id3[0],
                "tsiId": "00000000-0000-0000-0000-000000000000",  # Sometimes m
                "y": year,
                "m": month,
                "d": day,
                "t": "",
                "v": "0"}

            booking2 = requests.post('https://recreation.utoronto.ca/booking/reserve',
                                     headers={"accept": "*/*",
                                              "accept-encoding": "gzip, deflate, br",
                                              "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,und;q=0.4",
                                              "referer": "https://recreation.utoronto.ca/booking/%s" % court2_id,
                                              "origin": "https://recreation.utoronto.ca",
                                              "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                                              "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                                              "sec-ch-ua-mobile": "?1",
                                              "sec-ch-ua-platform": "'Android'",
                                              "sec-fetch-dest": "empty",
                                              "sec-fetch-mode": "cors",
                                              "sec-fetch-site": "same-origin",
                                              "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36",
                                              "x-requested-with": "XMLHttpRequest",
                                              "cookie": ".AspNet.ApplicationCookie=%s" % application_cookie,
                                              }, data=data2)


            booking1 = requests.post('https://recreation.utoronto.ca/booking/reserve',
                                    headers={"accept": "*/*",
                                             "accept-encoding": "gzip, deflate, br",
                                             "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,und;q=0.4",
                                             "referer": "https://recreation.utoronto.ca/booking/%s" % court1_id,
                                             "origin": "https://recreation.utoronto.ca",
                                             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                                             "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                                             "sec-ch-ua-mobile": "?1",
                                             "sec-ch-ua-platform": "'Android'",
                                             "sec-fetch-dest": "empty",
                                             "sec-fetch-mode": "cors",
                                             "sec-fetch-site": "same-origin",
                                             "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36",
                                             "x-requested-with": "XMLHttpRequest",
                                             "cookie": ".AspNet.ApplicationCookie=%s" % application_cookie,
                                             }, data=data1)



            booking3 = requests.post('https://recreation.utoronto.ca/booking/reserve',
                                    headers={"accept": "*/*",
                                             "accept-encoding": "gzip, deflate, br",
                                             "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,und;q=0.4",
                                             "referer": "https://recreation.utoronto.ca/booking/%s" % court3_id,
                                             "origin": "https://recreation.utoronto.ca",
                                             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                                             "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                                             "sec-ch-ua-mobile": "?1",
                                             "sec-ch-ua-platform": "'Android'",
                                             "sec-fetch-dest": "empty",
                                             "sec-fetch-mode": "cors",
                                             "sec-fetch-site": "same-origin",
                                             "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36",
                                             "x-requested-with": "XMLHttpRequest",
                                             "cookie": ".AspNet.ApplicationCookie=%s" % application_cookie,
                                             }, data=data3)
            # print(data)
            print("finished sending request")
            print(datetime.now())
            print(booking1.text)
            print(booking2.text)
            print(booking3.text)

        else:
            print("no data yet.")
            print(datetime.now())
            # print(timeslot_string)
            # time.sleep(0.05) #This line can be removed if need to aggressively compete with other bots.


def book_courts(book_hour, am_or_pm, court_id, fid):
    print("start booking courts")
    book_court()


def end_schedule():
    assert False


schedule.clear()
schedule.every(1).minutes.do(update_application_cookie)

for i, (book_hour, am_or_pm) in enumerate(zip(book_hours, am_or_pms)):
    if book_person == '1':
        if i <= 0:
            court_id = court2_id
            fid = court2_fid
        elif i <= 1:
            court_id = court3_id
            fid = court3_fid
        else:
            court_id = court1_id
            fid = court1_fid
    elif book_person == '2':
        if i <= 0:
            court_id = court1_id
            fid = court1_fid
        elif i <= 1:
            court_id = court2_id
            fid = court2_fid
        else:
            court_id = court3_id
            fid = court3_fid
    elif book_person == '3':
        if i <= 0:
            court_id = court3_id
            fid = court3_fid
        elif i <= 1:
            court_id = court1_id
            fid = court1_fid
        else:
            court_id = court2_id
            fid = court2_fid

    schedule.every().day.at("%02d:59:58" % (time_12to24[(book_hour, am_or_pm)] - 1)).do(book_courts,
                                                                                        book_hour=book_hour,
                                                                                        am_or_pm=am_or_pm,
                                                                                        court_id=court_id, fid=fid)
    if i == len(book_hours) - 1:
        schedule.every().day.at("%02d:00:01" % (time_12to24[(book_hour, am_or_pm)])).do(end_schedule)

while True:
    schedule.run_pending()
    time.sleep(0.05)

