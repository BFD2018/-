import requests,time,hashlib,random,os
from bs4 import BeautifulSoup
from threading import Thread

header = {"Cookie": "Hm_lvt_0dfa94cc970f5368ddbe743609970944=1559176088; bdshare_firstime=1559176207272",
          "Host": "www.xiaohuar.com",
          "Referer": "http://www.xiaohuar.com/",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3472.3 Safari/537.36"
          }

class XiaoHuaR(Thread):
    def __init__(self,filepath,url):
        super().__init__()
        self.filepath = filepath
        self.url = url

    def page_html(self,url):
        try:
            response = requests.get(url,headers = header)
            if response.status_code == 200:
                return response
        except Exception as e:
            print(e)
            pass

    def parse_all_items(self,url):
        html = self.page_html(url).text
        soup = BeautifulSoup(html,"lxml")
        items_list = soup.find(id="images").find_all(attrs={"class":"items"})
        items = []
        for item in items_list:
            try:
                page_url = item.a.attrs["href"]
                items.append(page_url)
            except:
                continue
        return items

    def get_movie_info(self,url):
        try:
            html = self.page_html(url).text
            soup = BeautifulSoup(html,"lxml")
            movie_url = soup.find(id="player").find(id="media").find('source').attrs["src"]
            movie_title = soup.find(attrs={"class":"contentinfo"}).find("h1").text+"."+movie_url.split(".")[-1]
            if not movie_title:
                md5 = hashlib.md5()
                md5.update(str(time.time()).encode('utf8'))
                movie_title = md5.hexdigest()
            return movie_title,movie_url
        except Exception as e:
            return None

    def saveTofile(self,path,url):
        byteContent = self.page_html(url).content
        with open(path,'wb') as f:
            f.write(byteContent)
            print("%s --->下载成功"%path)

    def run(self):
        items_list = self.parse_all_items(self.url)
        for item in items_list:
            path = self.filepath
            movie_info = self.get_movie_info(item)
            if movie_info:
                path = path + movie_info[0]
                print(movie_info)
                print(path)
                try:
                    self.saveTofile(path,movie_info[1])
                    time.sleep(random.randint(1,3))
                except:
                    continue


if __name__ == '__main__':
    if not os.path.exists("校花网小视频"):
        os.makedirs("校花网小视频")
    filepath = "校花网小视频\\"
    for i in range(10):
        url = "http://www.xiaohuar.com/list-3-{page_num}.html".format(page_num=i)
        xiaohua  = XiaoHuaR(filepath,url)
        xiaohua.start()

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>主")


