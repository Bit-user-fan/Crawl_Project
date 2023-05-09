import requests


PROXY_POOL_URL = 'http://localhost:5000/random'
TEST_URL = 'https://www.baidu.com/'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except  ConnectionError:
        return None

def use_proxy():
    proxy = get_proxy()
    if 'no proxy is available' in proxy:
        print('no proxy')
        return
    proxies = {
        'http':'http://' + proxy,
        'https':'http://' + proxy
    }
    try:
        response = requests.get(TEST_URL, proxies=proxies)
        print(response.status_code)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)

if __name__ == '__main__':
    use_proxy()

