#coding=utf-8
import re
import os
import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", help = "Input url like: http://test.com/")
parser.add_argument("-r", help = "Input a filename like: test.txt")
parser.add_argument("-cookie", help = "Input the cookie like: _uab_collina=159176874292860841473369; ")
args = parser.parse_args()

def connect_url(url):
    if args.cookie == None:
        html = requests.get(url, timeout = 5).text
    else:
        header = {
            "Cookie":args.cookie 
        } 
        html = requests.get(url, headers = header, timeout = 5).text
        
    return html


def testurl():
    '''
    a标签链接获取
    '''
    url = str(args.u)
    html = connect_url(url)
    #print(html)
    a_target = r'[htps]+://[a-zA-Z0-9\u4e00-\u9fa5\?\=\@\&\_\/\.\-\%\+\#]+'
    a_link = re.findall(a_target, html) 
    a_link = list(set(a_link))
    #print(html)

    '''
    短链接获取
    '''

    a_short_target = r'href=[\'|\"][\.\/]*[a-zA-Z0-9\u4e00-\u9fa5\?\=\&\_\/\.\-\%\+\#]+'
    a_short_link = re.findall(a_short_target, html)
    a_short_link = ','.join(a_short_link)
    a_short_link = re.sub(r'href=|\'|\"', "", a_short_link)
    a_short_link = a_short_link.split(',')
    a_short_link = list(set(a_short_link))
    
    
    '''
    JS 链接获取
    '''
    j_target = r'[htps:]*[\.\/]*[a-zA-Z0-9\u4e00-\u9fa5\?\=\&\@\_\/\.\-\%\#\+]+\.js'
    j_link = re.findall(j_target, html)
    j_link = ','.join(j_link)
    j_link = re.sub(r'href=|src=|\"|\'', "", j_link)
    j_link = j_link.split(',')
    j_link = list(set(j_link))
    
    print('\na-link: \n')
    for i in a_link:
        print(i)
    print('\n')
    print('------------------------------------------------------------------')
    
    print('\na-shortlink: \n')
    for i in a_short_link:
        print(i)
    print('\n')
    print('------------------------------------------------------------------')
    
    print('\nj-link: \n')
    for i in j_link:
        print(i)
    print('\n')

    return a_link, a_short_link, j_link


def get_target(target_file): 
    '''
    从本地获取链接进行爆破
    '''
    try:
        with open(target_file, "r", encoding='utf-8') as f:
            content = f.read().splitlines()
        return content
    except Exception as e:
        print("\nCan not find the file!\n")
        sys.exit(0)


def save_target(j_link, filename):
    '''
    JS文件写入
    '''
    symbol = '\n'
    f = open(filename, "w", encoding='utf-8')
    f.write(symbol.join(j_link))
    f.close()
    print('Save file successfully!\n')


def JS_edit(JSlist, url):
    '''
    JS链接整理
    '''
    for i in range(len(JSlist)):
        if re.search(r'http|https', JSlist[i]):
            pass
        else:
            JSlist[i] = url + JSlist[i]
    
    return JSlist


def sensitive_information(JSlist):
    '''
    访问js页面并抓取目录
    '''
    final_list = []
    for i in JSlist:
        try:
            html = connect_url(i)
            secret_url = re.findall(r'\.\/[a-zA-Z0-9\u4e00-\u9fa5\?\=\&\_\/\.\-\%\+\#]+', html)
            params1 = re.findall(r'\/[a-zA-Z0-9\u4e00-\u9fa5\?\=\&\_\/\.\-\%\+\#]+', html)
            secret_url += params1
            secret_url = list(set(secret_url))
            for i in secret_url:
                if len(i) > 50:
                    pass
                else:
                    final_list.append(i)
    

        except Exception as e:
            pass

    save_target(final_list,"url_list.txt")
    


def main():
    if args.u != None and args.r == None:
        a_target, a_short_target, js_target = testurl()
        save_target(js_target,"JS_list.txt")
        
    elif args.r != None and args.u == None:
        js_target = get_target(args.r)
        url = input('Input the target url: ')
        JSlist = JS_edit(js_target, url)
        print('\nCollecting.......\n')
        sensitive_information(JSlist)
          
    else:
        print('Use -h to get help.')


if __name__ == '__main__':
    main()
    
    