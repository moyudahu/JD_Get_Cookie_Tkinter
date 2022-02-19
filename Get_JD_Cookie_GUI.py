import tkinter as tk
import time
from  selenium  import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
import pyperclip
import chromedriver_autoinstaller
import threading
import os,sys

def run():
    global text
    text.delete(1.0,tk.END)#清空显示文本
    text.insert(tk.END,"程序开始运行...\n正在加载浏览器...\n加载过程中将启动chromedriver.exe和浏览器，请不要关闭它!")
    chromedriver_autoinstaller.install()
    text.insert(tk.END,"\n浏览器加载完毕")
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'browser' : 'ALL','performance' : 'ALL',}
    caps['perfLoggingPrefs'] = {'enableNetwork' : True,'enablePage':False,'enableTimeline': False}
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-single-click-autofill")
    option.add_argument("--enable-webgl --no-sandbox --disable-dev-shm-usage")
    option.add_argument("--disable-autofill-keyboard-accessory-view[8]")
    #option.binary_location=('Chrome\Application\chrome.exe')
    option.add_experimental_option('w3c',False)
    option.add_experimental_option('perfLoggingPrefs',{'enableNetwork':True,'enablePage':False,})
    option.add_experimental_option('excludeSwitches', ['enable-automation']) #禁止自动化提示框
    wd = webdriver.Chrome(options=option,desired_capabilities=caps)
    wd.set_window_size(360, 1000)
    #text.insert(tk.END,"Get Jd cookie \n by 摸鱼大户")
    text.insert(tk.END,"\n正在打开浏览器...\n请登陆获取COOKIE")
    url = 'https://plogin.m.jd.com/login/login'
    wd.get(url)  # 打开jd手机端登录网页，输入手机号，获取验证码
    while True:
        try:
            cookies = wd.get_cookies()  #  程序等待50秒后自动获取cookie
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            jd_cookie = '; '.join(item for item in cookie)
            p1 = r'(pt_pin=.+?;)'
            p2 = r'(pt_key=.+?);'
            jd_cookie =re.findall(p2, jd_cookie)[0]+";"+re.findall(p1, jd_cookie)[0]
            # 得到'pt_pin=xxxx;pt_key=xxxxxx'两项cookie值，可用于jd云函数/action自动签到
            if jd_cookie!="":
                pyperclip.copy(jd_cookie)
                text.insert(tk.END,"\n已经找到JD_cookie\n-----------↓↓↓↓↓↓---------\n\n")
                text.insert(tk.END,jd_cookie)
                text.insert(tk.END,"\n\n-----------↑↑↑↑↑↑--------\n\n")
                text.insert(tk.END,"\nCOOKIE已经自动复制到剪切板，请黏贴\n\n")
                #input("请按回车键关闭浏览器，关闭后浏览器将重新打开，如果新的COOKIE需要获取，请重新登陆\n....")
                wd.quit()  # 自动关闭浏览器
                break
            else:
                time.sleep(1)
            time.sleep(1)
        except:
            time.sleep(1)
   
def thread_it(func, *args):
  '''将函数打包进线程'''
  # 创建
  t = threading.Thread(target=func, args=args) 
  # 守护 !!!
  t.setDaemon(True) 
  # 启动
  t.start()
  # 阻塞--卡死界面！
  # t.join()
  
  
root = tk.Tk()
root.title("Get Jd Cookie --By：摸鱼大户")
root.geometry("360x360+800+100")
root.resizable(0,0)
#root.attributes("-alpha",0.90)
text = tk.Text(root)
text.pack()

  
tk.Button(root, text='开始运行',command=lambda :thread_it(run,)).pack()

def JieShu():
    text.insert(tk.END,"正在关闭程序...\n结束浏览器Chrome和Chormedriver后将关闭本程序...")
    os.system('taskkill /im chromedriver.exe /F')
    os.system('taskkill /im chrome.exe /F')
    sys.exit(0)
    #销毁root窗口
    root.destroy()
    #在此处下方可以写入结束线程的语句，如果开启了多线程的话。
 
#下面这一句最重要，是接收到关闭点击操作的语句,之后调用JieShu函数
root.protocol("WM_DELETE_WINDOW", JieShu)
root.mainloop()
