# To run file locally to book courts:
1. Clone this repo / download this repo
2. Then in your command prompt and cd to Badminton-Discord-Bot/cogs/CourtBookingFiles
3. Run python3 BookCourt.py month day [time] [PM or AM] 1 ".AspNet.ApplicationCookie"

Note: to get the .AspNet.ApplicationCookie
1. Login to recreation.utoronto.ca.
2. Once logged in, right-click anywhere on the webpage and select "Inspect".
3. Go to Application > Storage > Cookies > [https://recreation.utoronto.ca](https://recreation.utoronto.ca).
4. Find the Value for the cookie name ".AspNet.ApplicationCookie", and copy that value.

### Sample:
   python3 BookCourt.py 7 09 [9] [PM] 1 "lYm-IMUfJGAJFcD18HcUkA0VNNWoa5rukb-iRoRfsumh5nEYsVS9_QcpTqr9LevCnPW5xBDhjV8iGrbe9AKgvpG2ah1sR8Hh7kom0IcM0Cv6fNWpSeOtf_L1Ngn8wZnMuUNp1Ucv6zuFQCifqcizsndUfVMtY4PBeQWHwuIW3IuQ5_mp3BU0P7a67SljJuvoKd6yzq_O6EpO5hrKLN5T27dUhTE7jpps93c7fDowaJHrATO84EguiEkjUyBrYSeOAMEFWgiuiaBVeZDzlTiFDm0T5IzXnGkBnd9ha2mzGyWTOLywQTJK6nX7gGM7UuU-ae20w9PvrNOrInN5LvlJZR9hV8D5slvYVYMJVScaZ0PoRtSjLVeD4772lKLwFz-FDY_0NaG1qVf1yHtOj_lsSg" 
