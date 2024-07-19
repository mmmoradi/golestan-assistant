from golestan import Golestan

import pandas as pd
import requests
import datetime
from time import sleep


if __name__ == '__main__':
    g = Golestan()
    g.login()


    course = ['no','no']
    sleep(10)
    print("Start")


    while True:
        data = g.scores()

        if pd.isnull(data[8][2]):
            course[0] = 'no'
        else:
            course[0] = 'yes'

        if pd.isnull(data[8][4]):
            course[1] = 'no'
        else:
            course[1] = 'yes'


        now = datetime.datetime.now()
        url = f'http://status.mmahdim.ir/endpoint.php?kheradmandi={course[0]}&ahmadian={course[1]}&last_update={now}'
        print(url)
        print(requests.get(url))
        sleep(100)
