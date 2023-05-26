import os
from docx import Document
import shutil

def recognition(file):    

    #check = ['招标文件', '磋商文件', '项目编号', '项目名称'， '目录'，'文件格式']

    check = '文件格式'
    for para in file.paragraphs: 
        if check in para.text: 
            return True   
    return False
        
def regAll():
    ## 读取地址
    path = r"/home/albay/djs/data_docx/01/"
    save_path = r"/home/albay/djs/recog/01/"
    trash_path = r"/home/albay/djs/trash/01/"
    
    for file in os.listdir(path): 
        try: 
            read_file = Document(path + file)
            tf = recognition(read_file)
            if tf == True: 
                copy_file = path + file
                shutil.copy(copy_file, save_path)
                print("{0} is copied and saved".format(copy_file))
            else:
                copy_file = path + file
                shutil.copy(copy_file, trash_path)
        except Exception as e:
            print('Error: ', e)


if __name__ == '__main__': 
    regAll()
