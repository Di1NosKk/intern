from pdf2docx import Converter
import os
import shutil
import subprocess
from docx import Document
import time
import datetime
import signal
from contextlib import contextmanager
import pytz
from concurrent.futures import ProcessPoolExecutor
import pdfplumber


class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def get_pdf_page_count(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            return page_count
    except Exception as e:
        # print(f"Error: An error occurred while processing PDF file '{file_path}'. Reason: {str(e)}")
        return 0

def pdftodocx(pdf, docx, file):
    print("当前pdf：{}----> started at {}".format(file, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    try:
        with time_limit(30):
            cv = Converter(pdf)
            cv.convert(docx)
            cv.close()
    except Exception as e:
        print("Timed out! or other! exception is {} and file is {}".format(e, file))
                

def convert_to_docx(path, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    
    task = []
    
    with ProcessPoolExecutor(max_workers=10) as executor:
        for file in os.listdir(path):
            ## 后缀
            suff = os.path.splitext(file)[1]
            # pdf转docx
            if suff == '.pdf': 
                file_name = os.path.splitext(file)[0]
                pdf_file = path + file_name + suff
                docx_file = save_path + file_name + '.docx'
                stats = os.stat(pdf_file)
                if stats.st_size >= 52428800:
                    continue
                if get_pdf_page_count(pdf_file) == 0:
                    print("Broken File: {}".format(file))
                    continue
                result = executor.submit(pdftodocx, pdf_file, docx_file, file)
                task.append(result)
                
    while True:
        exit_flag = True
        for t in task:
            if not t.done():
                exit_flag = False
        if exit_flag:
            print("finished at {}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            break
        
def recognition(file):    

    #check = ['招标文件', '磋商文件', '项目编号', '项目名称'， '目录'，'文件格式']

    check = '文件格式'
    for para in file.paragraphs: 
        if check in para.text: 
            return True   
    return False
    
        
def recogAll(path, save_path):
    ## 读取地址
    
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    
    for file in os.listdir(path): 
        try: 
            read_file = Document(path + file)
            tf = recognition(read_file)
            if tf == True: 
                copy_file = path + file
                shutil.copy(copy_file, save_path)
                print("{0} is copied and saved in {1}".format(file, save_path))
        except Exception as e:
            print('Error: ', e)

    
def main():
    today = datetime.datetime.today().astimezone(pytz.timezone('Etc/GMT-8'))
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime('%Y/%m/%d')
    lst = yesterday.split("/")
    year = lst[0]
    month = lst[1]
    day = lst[2]
    date = yesterday + "/"
    path1 = r"/data/data/purchase_resource/Purchase/"
    
    read_path = path1 + date
    save_path = r"/data/data/zhaobiao_book_tmp_pdf/" + date
    
    path2 = r"/data/data/purchase_resource/Purchase_zhaobiao_book/"
    bid_path = path2 + date
    
    print(read_path)
    print(save_path)
    print(bid_path)
    
    convert_to_docx(read_path, save_path)
    recogAll(save_path, bid_path)
    
    print("finished")

if __name__ == '__main__':
    main()

