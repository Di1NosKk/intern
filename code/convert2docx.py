from pdf2docx import parse
import os
import shutil
import subprocess


def convert_to_docx():
    ## 原地址
    path = r"/home/albay/djs/data/01/"
    ## 存储地址
    save_path = r"/home/albay/djs/data_docx/01/"
    
    for file in os.listdir(path):
        ## 后缀
        suff = os.path.splitext(file)[1]
        
        ## pdf转docx
        if suff == '.pdf': 
            file_name = os.path.splitext(file)[0]
            pdf_file = path + file_name + suff
            docx_file = save_path + file_name + '.docx'
            parse(pdf_file, docx_file)
        ## doc转docx
        elif suff == '.doc': 
            file_name = os.path.splitext(file)[0]
            doc_file = path + file_name + suff
            os.system("soffice --headless --convert-to docx %s --outdir %s" % (doc_file, save_path))
        ## docx复制到储存地址
        elif suff == '.docx':
            copy_file = path + file
            shutil.copy(copy_file, save_path)
        else: 
            continue
        
        

if __name__ == '__main__': 
    convert_to_docx()
