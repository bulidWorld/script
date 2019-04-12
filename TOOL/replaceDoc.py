import re

import zipfile
import os

#替换表达式
def replaceOth(filePath):
    f = open(filePath, 'r', 10240, 'UTF-8')
    str = f.read()
    f.close()

    re.DOTALL = True
    pattern = re.compile(r'\$\{[\s\S]*?\}')
    mchLst = pattern.findall(str)

    for ele in mchLst:
        mch = re.search(r'<w:t>.*</w:t>', ele)
        if (mch != None):
            relVal = '${' + mch.group()[5:-6] + '!}'
            str = str.replace(ele, relVal)
        if ele.find('informfactoringflag_2') != -1 :
            str = str.replace(ele, '${informfactoringflag_2!}')
    print(mchLst)
    print(str)

    f = open(filePath, 'w', 10240, 'UTF-8')
    f.write(str)
    f.close()


#解压缩并且替换表达式
def extract_and_replace_str(dir):
    file_list = os.listdir(dir)
    for file_name in file_list:
        if os.path.splitext(file_name)[1] == '.docx' and  not file_name.startswith('~'):

            file_zip = zipfile.ZipFile(dir + '\\' + file_name, 'r')

            extracted_dir = dir + '\\' + file_name.replace('.docx', '')
            for file in file_zip.namelist():

                file_zip.extract(file, extracted_dir)

                if file == 'word/document.xml':
                    extracted_doc_path = extracted_dir + '/' + file
                    replaceOth(extracted_doc_path)
            file_zip.close()
            os.remove(dir + '\\' + file_name)


#压缩目录下的所有文件夹
def zip_dir_all_file(dir):
    file_list = os.listdir(dir)
    for file_name in file_list:

        if file_name.endswith('.docx'):
            continue

        startdir = dir + '/' + file_name  # 要压缩的文件夹路径
        file_news = startdir + '.docx'  # 压缩后文件夹的名字
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                print('压缩成功')
        z.close()


# 删除多出来的标签内容
# dir = 'F:/t3'
# extract_and_replace_str(dir)
# zip_dir_all_file(dir)

# replaceOth('F:\\t2\\2-N-T\\word\\document.xml')


# 检查替换是否cedilla
def checkContainSpe(dir):
    file_list = os.listdir(dir)
    for file_name in file_list:
        if os.path.splitext(file_name)[1] == '.docx' and not file_name.startswith('~'):

            file_zip = zipfile.ZipFile(dir + '\\' + file_name, 'r')

            extracted_dir = dir + '\\' + file_name.replace('.docx', '')
            for file in file_zip.namelist():

                file_zip.extract(file, extracted_dir)

                if file == 'word/document.xml':
                    extracted_doc_path = extracted_dir + '/' + file
                    docFile = open(extracted_doc_path, 'r', 10240, 'UTF-8')
                    str = docFile.read()
                    docFile.close()
                    if str.find('{') != -1:
                        print(file_name)
            file_zip.close()
            # os.remove(dir + '\\' + file_name)

checkContainSpe('F:/t4')