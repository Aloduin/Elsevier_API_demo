import time
import requests
import os
# import xlrd
# import xlwt
import pandas as pd
from tqdm import tqdm, trange

# def ensure_path_exits(path: str):
#     if not os.path.exists(path):
#     # 创建目录
#         os.makedirs(path)
#     return

class ArticleArchiveDoi:
    def __init__(self, header, filename, url_publisher, apikey, arformat, path, text_outpath):
        self.filename = filename
        self.url_publisher = url_publisher
        self.apikey = apikey
        self.arformat = arformat
        self.path = path
        self.header = header
        self.out_path = text_outpath

    def data_totxt(self, sample, path):
        f = open(path, 'w', encoding='utf-8')
        f.write(sample)
        f.close()

    # def httprequest(self):
    #     xls = xlwt.Workbook()
    #     sheet = xls.add_sheet("doi-text_path")
    #     data = xlrd.open_workbook(self.filename)
    #     table = data.sheet_by_index(0)
    #     list_values = []
    #     for x in trange(1, len(table.col_values(1))):
    #         values = []
    #         row = table.row_values(x)
    #         values.append(row[1])
    #         list_values.append(values)
    #     dois = list_values
    #     # print(dois)
    #     count = len(dois)
    #     for i in trange(0, count):
    #         url = self.url_publisher + dois[i][0] + "?" + self.apikey + "&httpAccept=" + self.arformat
    #         try:
    #             r = requests.get(url, headers=self.header, timeout=100)
    #         except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout):
    #             while(int(r.status_code) != 200):
    #                 r = requests.get(url, headers=self.header, timeout=100)
    #         content = r.content.decode()
    #         print(self.path)
    #         path = self.path + '/' + dois[i][0] + '.xml'
    #         print(path)
    #         self.data_totxt(content, path)
    #         sheet.write(i, 0, dois[i][0])
    #         sheet.write(i, 1, path)
    #     xls.save(self.out_path)


    def httprequest(self):
        xls = pd.read_excel(self.filename, index_col=0)
        # 记录需要下载文件的doi
        dois_list = [row[0] for _, row in xls.iterrows()]
        downloaded_file = []
        download_error_doi = []
        # 设置最大重试次数
        max_retries = 30
        
        for doi in tqdm(dois_list):
            url = self.url_publisher + doi + "?" + self.apikey + "&httpAccept=" + self.arformat
            # try:
            #     r = requests.get(url, headers=self.header, timeout=100)
            # except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout):
            #     while(int(r.status_code) != 200):
            #         r = requests.get(url, headers=self.header, timeout=100)
            
            retries = 0
            while retries < max_retries:
                
                try:
                    r = requests.get(
                        url=url,
                        headers=self.header,
                    )
                    break
                    
                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.Timeout,
                    requests.exceptions.HTTPError,
                    requests.exceptions.RequestException,
                ):
                    print("Retring...")                    
                    retries += 1
                    time.sleep(30)
            if retries == max_retries:
                download_error_doi.append(
                    {
                        "doi": doi
                    }
                )
                continue
            content = r.content.decode()
            
            file_name = self.path +'/' + doi[8:] + '.xml'
            self.data_totxt(content, file_name)
            downloaded_file.append(
                {
                    'doi': doi,
                    'path': file_name,
                }
            )
            
        df = pd.DataFrame(downloaded_file)
        df.to_excel(self.out_path)
        error_df = pd.DataFrame(download_error_doi)
        error_df.to_excel("error_doi.xlsx")
