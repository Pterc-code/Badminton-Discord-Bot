To run file locally to book courts:
    1. Clone this repo / download this repo
    2. Then in your command prompt and cd to Badminton-Discord-Bot/cogs/CourtBookingFiles
    3. Run 
    python3 BookCourt.py month day "[time]" "[PM or AM]" "1" ".AspNet.ApplicationCookie"

    Note: to get the .AspNet.ApplicationCookie
    1. Login to recreation.utoronto.ca.
    2. Once logged in, right-click anywhere on the webpage and select "Inspect".
    3. Go to Application > Storage > Cookies > [https://recreation.utoronto.ca](https://recreation.utoronto.ca).
    4. Find the Value for the cookie name ".AspNet.ApplicationCookie", and copy that value.

    Sample:
    python3 BookCourt.py 7 7 "[6]" "[PM]" "1" "WSlHrgv5ffPeCn3PPp4O264VEP0qSylDoym-XmfI8jCdrXOcZlf6wskelQNQ1fq7DWqQWvyJZ-sd4KJSYh1oOcLCgVHel4KflaSQZpZ4RQ16ht2ro9qMIgfNupOgSjMQffb2ZkprQ5Q7APRrRB92NL7cyW10OATPVgHGgwhXjIgRq1gbKk_LjNA-DNEp2K5miLx9gz0evKj9x0Tb-NRkdUeSAhN7aSDS9-ByfA7tY6GmlmDqisFj3FjImCLGM-mtrQmL7pxDXLEauJhUbiIEkFCZtJ8ShG_2MCozhja2W_wr6whbe1dpdybIhrEUkXRozLTqN5mFl4f_6Y2N-EUBUWYag0sksp9CjwehAXc5t2XGh4WyFVDjIoUvBPXDHd14Wa7YmC9Vn_iJD6UnM0X2IQ"