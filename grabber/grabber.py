import requests
import strtotime
from models import Plurk
from tqdm import tqdm
import datetime
import time


def main():
    while True:
        print("start grabbing")
        # print(strtotime.strtodatetime('Tue, 24 Nov 2020 06:11:33 GMT').timestamp())
        min_offset = 0
        hit = False
        for i in tqdm(range(500)):
            if hit:
                break
            r = requests.get(
                'https://www.plurk.com/Stats/getAnonymousPlurks?lang=zh&offset={}&limit=200'.format(min_offset))
            data = r.json()
            buffer = []
            for key in data:
                if key not in ['pids', 'count']:
                    plurk = data[key]
                    # plurk['plurk_id'] #plurk id int
                    # plurk['posted'] #posted datetime
                    # plurk['content'] #content
                    # plurk['content_raw'] #content raw
                    if Plurk.select().where(Plurk.id == plurk['plurk_id']).exists():
                        hit = True
                        continue
                    else:
                        timestamp = int(strtotime.strtodatetime(
                            plurk['posted']).timestamp())
                        new_plurk = {'id': plurk['plurk_id'],
                                    'posted': timestamp,
                                    'content': plurk['content'],
                                    'content_raw': plurk['content_raw']}
                        buffer.append(new_plurk)
            Plurk.insert_many(buffer).execute()
            min_offset = min([*data['pids'], min_offset])
        print('sleeping')
        for i in tqdm(range(15*60)):
            time.sleep(1)


if __name__ == '__main__':
    main()
