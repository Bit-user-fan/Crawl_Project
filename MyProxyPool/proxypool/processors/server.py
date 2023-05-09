from flask import Flask
import json
import random

app = Flask(__name__)

def get_conn():
    try:
        with open('../storages/proxydict.json', mode='r', encoding='utf-8') as fp:
            proxydict = json.loads(fp.read())
        proxy_valid = []
        for proxy in proxydict.keys():
            if proxydict[proxy] == 100: # 将100分的代理加入有效代理列表
                proxy_valid.append(proxy)
        return proxy_valid
    except FileNotFoundError:
        return 'FileNotFound'


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    conn = get_conn()
    if conn == 'FileNotFound': # 此时proxydict.json文件还未生成，即代理还未爬取到，提示等待
        return '<h2>No proxy has been obtained, please wait</h2>'
    if not conn: # conn为[],代理中不存在分数为100的代理，即代理池中的代理对测试网站均不可用
        return '<h2>No proxy is available</h2>'
    return random.choice(conn)

if __name__ == '__main__':
    app.run()