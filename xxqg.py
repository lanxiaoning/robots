# _*_ coding: utf-8 _*_

from selenium import webdriver
import sys
import time
import datetime
import pickle
import os
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

__author__ = 'lanxiaoning'


HOME_PAGE = 'https://www.xuexi.cn/'

#VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html?pageNumber=39'

VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html'

LONG_VIDEO_LINK = 'https://www.xuexi.cn/f65dae4a57fe21fcc36f3506d660891c/b2e5aa79be613aed1f01d261c4a2ae17.html'

LONG_VIDEO_LINK2 = 'https://www.xuexi.cn/0040db2a403b0b9303a68b9ae5a4cca0/b2e5aa79be613aed1f01d261c4a2ae17.html'

TEST_VIDEO_LINK = 'https://www.xuexi.cn/8e35a343fca20ee32c79d67e35dfca90/7f9f27c65e84e71e1b7189b7132b4710.html'

SCORES_LINK = 'https://pc.xuexi.cn/points/my-points.html'

LOGIN_LINK = 'https://pc.xuexi.cn/points/login.html'

##头条新闻更新频率低，使用重要新闻代替
##ARTICLES_LINK = 'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html'
ARTICLES_LINK = 'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html'

MY_STUDY='https://pc.xuexi.cn/points/my-study.html'

##滚动900单位
SCROLLS=900
##有效阅读时间为2分钟
ARTICAL_READ_TIME=120
##有效视频观看3分钟
VIDEO_WATCH_TIME=180
MAX_TRY=7
##随机概率，如果(0,RAND_PER)之间的随机数是0，则执行doRandom()快速的阅读和关闭，不赚积分
RAND_PER=6
##cookie内容保存文件定义
COOKIE_FILE='xuexi.cookie'
TIMEOUT=30

driver='Application\\chromedriver.exe'

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-automation'])

#browser = webdriver.Chrome(executable_path=r'D:\OneDrive\Python\selenium\chromedriver.exe',options=options)
browser = webdriver.Chrome(executable_path=driver,options=options)


def login():
    browser.get(LOGIN_LINK)
    browser.maximize_window()
    browser.execute_script("var q=document.documentElement.scrollTop="+str(SCROLLS))
    print('请使用手机强国学习APP扫描登陆')
    ##登陆后会跳转到一个URL可以用来判断是否完成登陆
    while (browser.current_url != MY_STUDY):
        time.sleep(1)
    print('用户已登陆')


def watch_videos():
    print('开始观看视频')
    browser.get(VIDEO_LINK)
    time.sleep(1)
    p_window = browser.current_window_handle
    title_path='//*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[rownum]/div[colnum]/div/div/div[1]/span'
    for i in range(1,5):
        ##每行两条视频标题
        for j in range(1,3):
            titletmp = title_path.replace('rownum', str(i))
            title = titletmp.replace('colnum', str(j))
            ###使用WebDriverWait等待来替代自写的等待
            ##autoclick(title, 0)
            WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, title))).click()
            windows = browser.window_handles
            browser.switch_to.window(windows[-1])

            if (random.randint(0, RAND_PER) == 0):
                doRandom(browser, p_window)
                continue

            browser.execute_script("var q=document.documentElement.scrollTop=" + str(SCROLLS/2))

            ##有时候视频控件加载出来，但视频内容未加载，统计到class=duration的为00:00，所以还是要等待3秒
            time.sleep(3)

            # 点击播放....已改为自动播放
            #browser.find_element_by_xpath("//div[@class='outter']").click()

            # 获取视频时长
            #video_duration_str = browser.find_element_by_class_name('duration').get_attribute('innerText')
            ##video_duration_str=autotextbyclass('duration',0)
            ##使用WebDriverWait代替自编写的等待
            video_duration_str = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'duration'))).get_attribute('innerText')
            ##print('duration:'+video_duration_str)
            video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])
            print('视频时长:'+str(video_duration)+'秒,等待'+str(video_duration)+'秒')
            time.sleep(video_duration)

            ##如果视频时长过短，无法获取视听时长积分，则补回这个时间差
            if(video_duration<VIDEO_WATCH_TIME):
                print('视频时长不足，额外等待' + str(VIDEO_WATCH_TIME-video_duration) + '秒')
                waittime=VIDEO_WATCH_TIME-video_duration
                ##增加随机等待的时间
                randwaittime = random.randint(0, 5)
                waittime=waittime+randwaittime
                for k in range(0,waittime):
                    js_code = "var q=document.documentElement.scrollTop=" + str(k * 100)
                    browser.execute_script(js_code)
                    time.sleep(1)

            browser.close()
            browser.switch_to.window(p_window)

def read_articles():
    print('开始阅读文章')
    browser.get(ARTICLES_LINK)
    time.sleep(1)
    p_window=browser.current_window_handle
    title_path='//*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/section/div/div/div[1]/div/div[num]/div/div/div[1]/span'
    for i in range(1,7):
        title=title_path.replace('num',str(i))
        ###autoclick(title, 0)
        ###使用WebDriverWait代替自编写的等待
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, title))).click()
        windows = browser.window_handles
        browser.switch_to.window(windows[-1])

        if(random.randint(0,RAND_PER)==0):
            doRandom(browser,p_window)
            continue

        starttime=datetime.datetime.now()
        ##滚动条往下滚60秒
        for j in range(0, 60, 1):
            js_code = "var q=document.documentElement.scrollTop=" + str(j*40)
            browser.execute_script(js_code)
            time.sleep(1)

        ##滚动条再往上滚
        for k in range(60, 0, -1):
            js_code = "var q=document.documentElement.scrollTop=" + str(k*40)
            browser.execute_script(js_code)
            time.sleep(1)

        endtime = datetime.datetime.now()

        ##检查阅读时长，如果时长不足2分钟，则无法获取文章学习时长积分，需要补回时间差
        readtime=(endtime-starttime).seconds
        if(readtime<ARTICAL_READ_TIME):
            print('阅读时长不足，额外等待'+str(ARTICAL_READ_TIME-readtime)+'秒')
            time.sleep(ARTICAL_READ_TIME-readtime)

        ##随机事件，随机等待一定时间，在这段时间内自动滚动
        randwaittime=random.randint(0,5)
        for m in range(0,randwaittime):
            js_code = "var q=document.documentElement.scrollTop=" + str(m * 100)
            browser.execute_script(js_code)
            time.sleep(1)

        browser.close()
        browser.switch_to.window(p_window)

    print('阅读文章完毕')


##自动尝式点击一个XPATH，如果失败则再尝试，最多尝试MAX_TRY次
def autoclick(xpath,alreadytrycount):
    try:
        browser.find_element_by_xpath(xpath).click()
    except:
        if(alreadytrycount<MAX_TRY):
            time.sleep(1)
            alreadytrycount=alreadytrycount+1
            autoclick(xpath, alreadytrycount)
        else:
            print('经多次尝试，无法打定位元素'+xpath)
            sys.exit(-1)

def autotextbyclass(classname,alreadytrycount):
    try:
        textstr = browser.find_element_by_class_name(classname).get_attribute('innerText')
        return textstr
    except:
        if(alreadytrycount<MAX_TRY):
            time.sleep(1)
            alreadytrycount=alreadytrycount+1
            autotextbyclass(classname, alreadytrycount)
        else:
            print('经多次尝试，无法打定位元素'+classname)
            sys.exit(-1)

def get_scores():

    """获取当前积分"""

    browser.get(SCORES_LINK)

    '''

    time.sleep(2)

    gross_score = browser.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]").get_attribute('innerText')
    
    today_score = browser.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')
    
    '''

    gross_score=WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]"))).get_attribute('innerText')

    today_score=WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//span[@class='my-points-points']"))).get_attribute('innerText')

    print("当前总积分：" + str(gross_score))

    print("今日积分：" + str(today_score))

    print("获取积分完毕，即将退出\n")

def save_cookie():
    cookies=browser.get_cookies()
    print("开始保存cookie! ",cookies)
    pkCookies=pickle.dumps(cookies)
    with open(COOKIE_FILE,'wb+') as f:
        f.write(pkCookies)
        print("cookie已保存！")

def read_cookie():
    with open(COOKIE_FILE,'rb') as f:
        pkCookies=pickle.load(f)
        print("开始读取cookie! ")
        for item in pkCookies:
            #print('cookie item: '+str(item))
            if ('expiry' in item) and (item['expiry'] != (int(item['expiry']))):
                #print("修改前：", item)
                # 学习强国返回的expiry有小数，去掉
                item['expiry'] = int(item['expiry'])
                #print("修改后：", item)
                browser.add_cookie(item)
            else:
                #print("未修改：",item)
                browser.add_cookie(item)

##增加随机事件，使用一定的概率来打开页面后不做过多停留，快速关闭页面，增加拟人程度
def doRandom(b,p_w):
    print('进入随机操作模式')
    begintime = datetime.datetime.now()
    playtime=random.randint(1,5)
    for i in range(0, playtime):
        js_code = "var q=document.documentElement.scrollTop=" + str(i * 100)
        b.execute_script(js_code)
        time.sleep(1)
    b.close()
    b.switch_to.window(p_w)
    endtime = datetime.datetime.now()
    spenttime=(endtime-begintime).seconds
    print('退出随机操作模式，一共耗时'+str(spenttime)+'秒')

if __name__ == '__main__':

    if (os.path.exists(COOKIE_FILE)):
        print("cookie存在！")
        ##把COOKIE加载进浏览器之前，一定要先打开页面，否则会报invalid cookie domain
        browser.get(HOME_PAGE)
        browser.maximize_window()
        # 读cookie
        read_cookie()
        print("读完cookie，检测是否已有登陆信息!")
        try:
            browser.get(SCORES_LINK)
            #time.sleep(3)
            ##检查一下我的积分页面有没有退出按钮
            #element=browser.find_element_by_xpath('//*[@id="Ca6ke9htmh6800"]')
            ##等待“退出”按钮10秒
            element = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Ca6ke9htmh6800"]')))
        except:
            print('cookie可能已过期，需重新用手机APP扫描登陆')
            #删除cookie文件
            os.remove(COOKIE_FILE)
            # 模拟登录
            login()
            save_cookie()
    else:
        print("cookie不存在，进入登录页面！")
        # 模拟登录
        login()
        save_cookie()

    # 阅读文章
    read_articles()

    # 观看视频
    watch_videos()

    # 获得今日积分
    get_scores()

    # 更新cookie
    save_cookie()

    browser.quit()
