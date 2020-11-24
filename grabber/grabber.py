import requests
import strtotime

def main():
    print("start grabbing")
    # print(strtotime.strtodatetime('Tue, 24 Nov 2020 06:11:33 GMT').timestamp())
    r = requests.get('https://www.plurk.com/Stats/getAnonymousPlurks?lang=zh&offset=1457560198&limit=200')
    print(r.json())

if __name__ == '__main__':
    main()