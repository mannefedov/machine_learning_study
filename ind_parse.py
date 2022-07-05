import os
import requests
import re
from datetime import datetime
from time import sleep


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" beep'
              """.format(text, title))
    os.system('say slot found!')

def look():
    current = datetime.fromisoformat('2022-08-11').date() # current appointment date
    closest_possible_day = max([datetime.now().date(), # today or some other day in future
                                datetime.fromisoformat('2022-07-03').date() ])

    r = requests.get('https://oap.ind.nl/oap/api/desks/AM/slots/?productKey=DOC&persons=2',timeout=10)
    dates = set(re.findall('"date":"(.+?)"', r.text))
    if not dates:
        print('No slots at all!', datetime.now())

        return 
    
    dates = [datetime.fromisoformat(date).date() for date in dates]
    print('Closest open -', min(dates), '##', datetime.now())
    for date in dates:
        if date < current and date >= closest_possible_day:
            print('slot found! ', date, datetime.now())
            return str(min(dates))
    
def main():
    while True:

        d = look()
        if d:
            notify('IND', d)
        sleep(300)

if __name__ == '__main__':
    main()