import os

if __name__ == '__main__':
    os.system("scrapy crawl people")
#nohup python -u main.py > run.log 2>&1 &