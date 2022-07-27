import pandas as pd
import requests
from pathlib import Path

class FileSaver:
    def __init__(self, pic_dir_path ='./img/'):
        self.pic_dir_path = Path(pic_dir_path)
        self.cur_file_path ="" #dir below /img/ to save comments and imgs seperately

        if not self.pic_dir_path.exists(): #make sure the pic directory exists
            self.pic_dir_path.mkdir(parents=True, exist_ok=True)

    def set_item(self, scrapy_item)->None:
        self.cur_item = scrapy_item
        self.file_name = self.cur_item["article_title"] + " " + self.cur_item["author_name"]
        self.cur_file_path = self.pic_dir_path / self.file_name

    def check_dir_exist(self, file_name)->bool:
        return (self.pic_dir_path/file_name).exists()

    def save_comments_to_file(self)-> None:
        if not self.check_dir_exist(self.file_name): #make dir to save

            self.cur_file_path.mkdir(parents=True, exist_ok=True)

        comments = pd.DataFrame(self.cur_item["comments"])
        comments.to_csv(str(self.cur_file_path)+'/'+self.file_name+".csv",encoding='utf-8-sig')

    def save_imgs(self)->None:
        pic_urls = self.cur_item["pic_urls"]
        pic_urls_pd = pd.DataFrame(pic_urls)
        pic_urls_pd.to_csv((str(self.cur_file_path)+'/'+self.file_name+"img_urls"+".csv"))


        for num in range(len(pic_urls)):
            pic = requests.get(pic_urls[num]).content
            post_fix = pic_urls[num].split(".")[-1].lower() #用.來斷詞 抓最後一個當post fix
            if post_fix in ["jpg", "gif", "jpeg", "bmp", "png"]: #只抓圖檔跟動圖
                with open(str(self.cur_file_path)+'/'+f"{num}"+f".{post_fix}", 'wb') as f:
                    # 將圖片下載下來
                    f.write(pic)

