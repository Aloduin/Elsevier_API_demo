import os
from article_dois import ArticleArchiveDoi


def mkdir(file_name):
    pathd = os.getcwd()+'\\'+file_name
    if os.path.exists(pathd):
        for root, dirs, files in os.walk(pathd, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name)) 
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(pathd) 
    os.mkdir(pathd)



if __name__ == '__main__':
    folder1 = 'text_path'
    mkdir(folder1)
    folder2 = 'all_origin_txt'
    mkdir(folder2)
    filename = 'missing.xlsx'
    path_txt = r'all_origin_txt'
    file_excel = r'text_path\text_path.xls'
    header = {'Accept': 'text/xml', 'CR-TDM-Rate-Limit': '4000', 'CR-TDM-Rate-Limit-Remaining': '76', 
              'CR-TDM-Rate-Limit-Reset': '1378072800'}
    url_publisher = "https://api.elsevier.com/content/article/doi/"  # 如果获取全文的话，将abstract替换成article
    APIKey = "APIKey="   # developer Elsevier 申请的
    arformat = "text/xml"   # XML:text/xml;TXT:text/plain
    Article_archive_doi = ArticleArchiveDoi(header, filename, url_publisher, APIKey, arformat, path_txt, file_excel)
    Article_archive_doi.httprequest()
