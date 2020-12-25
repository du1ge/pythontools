#coding:utf-8
import re
import sys
text='' # 字符串
filename = '' # 源文件名
outputname = '' # 导出的文件名
INPUT_INFO = sys.argv

try:
    if len(INPUT_INFO) == 2:
        name = INPUT_INFO[1]
        filename, outputname = [i for i in name.split(',')] # 分别赋值给 filename, outputname
        try:
            with open(filename,"r",encoding='utf-8') as f1:
                for content in f1:
                    text += content
            print('\n')
            print('原始文件：' + filename)
            print('已导出到：' + outputname)
        
            text = re.sub(r'\d+\d+\d+B', "", text)
            text = re.sub(r'\d+B', "", text)
            text = re.sub(r'\d+KB', "", text)
            text = re.sub(r'\d+\d+\d', "", text)
            text = re.sub(r'-> REDIRECTS TO: +.*',"",text)
            text = re.sub(r' ',"",text)

            with open(outputname, "w", encoding='utf-8') as f:
                f.write(str(text))
                f.close()
            print('导出完成！')

        except Exception as ex:
            print('\n')
            print('源文件不存在！请检查！')
       
    else:
        print('\n')
        print('输入原始文件名,需要导出的文件名\n以","分隔,请按规则输入！')
        print('例如：python3 daochu.py 1.txt,2.txt')
        
except Exception as ex:
    print('\n')
    print('输入原始文件名,需要导出的文件名\n以","分隔,请按规则输入！')
    print('例如：python3 daochu.py 1.txt,2.txt')
