# _*_ coding: utf-8 _*_

from selenium import webdriver
import sys
import time

__author__ = 'lanxiaoning'


HOME_PAGE = 'https://www.xuexi.cn/'

#VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html?pageNumber=39'

VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html'

LONG_VIDEO_LINK = 'https://www.xuexi.cn/f65dae4a57fe21fcc36f3506d660891c/b2e5aa79be613aed1f01d261c4a2ae17.html'

LONG_VIDEO_LINK2 = 'https://www.xuexi.cn/0040db2a403b0b9303a68b9ae5a4cca0/b2e5aa79be613aed1f01d261c4a2ae17.html'

TEST_VIDEO_LINK = 'https://www.xuexi.cn/8e35a343fca20ee32c79d67e35dfca90/7f9f27c65e84e71e1b7189b7132b4710.html'

SCORES_LINK = 'https://pc.xuexi.cn/points/my-points.html'

LOGIN_LINK = 'https://pc.xuexi.cn/points/login.html'

ARTICLES_LINK = 'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html'

MY_STUDY='https://pc.xuexi.cn/points/my-study.html'

SCROLLS=900

MAX_TRY=7

driver='C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe'

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-automation'])

#browser = webdriver.Chrome(executable_path=r'D:\OneDrive\Python\selenium\chromedriver.exe',options=options)
browser = webdriver.Chrome(executable_path=driver,options=options)


def login_simulation():

    """模拟登录"""

    # 方式一：使用cookies方式

    # 先自己登录，然后复制token值覆盖

    # cookies = {'name': 'token', 'value': ''}

    # browser.add_cookie(cookies)



    # 方式二：自己扫码登录

    browser.get(LOGIN_LINK)

    browser.maximize_window()

    browser.execute_script("var q=document.documentElement.scrollTop="+str(SCROLLS))

    #time.sleep(10)

    waitlogin(True)

    browser.get(HOME_PAGE)

    print("模拟登录完毕\n")


def watch_videos():

    """观看视频"""

    browser.get(VIDEO_LINK)

    videos = browser.find_elements_by_xpath("//div[@id='Ck3ln2wlyg3k00']")

    spend_time = 0



    for i, video in enumerate(videos):

        if i > 6:

            break

        video.click()

        all_handles = browser.window_handles

        browser.switch_to_window(all_handles[-1])

        browser.get(browser.current_url)



        # 点击播放

        browser.find_element_by_xpath("//div[@class='outter']").click()

        # 获取视频时长

        video_duration_str = browser.find_element_by_xpath("//span[@class='duration']").get_attribute('innerText')

        video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])

        # 保持学习，直到视频结束

        time.sleep(video_duration + 3)

        spend_time += video_duration + 3

        browser.close()

        browser.switch_to_window(all_handles[0])



    # if spend_time < 3010:

    # browser.get(LONG_VIDEO_LINK)

    # browser.execute_script("var q=document.documentElement.scrollTop=850")

    # try:

    # browser.find_element_by_xpath("//div[@class='outter']").click()

    # except:

    # pass

    #

    # # 观看剩下的时间

    # time.sleep(3010 - spend_time)

    browser.get(TEST_VIDEO_LINK)

    time.sleep(3010 - spend_time)

    print("播放视频完毕\n")


def watch_videos2():
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
            autoclick(title, 0)
            windows = browser.window_handles
            browser.switch_to.window(windows[-1])

            browser.execute_script("var q=document.documentElement.scrollTop=" + str(SCROLLS))

            ##有时候视频控件加载出来，但视频内容未加载，统计到class=duration的为00:00，所以还是要等待3秒
            time.sleep(3)

            # 点击播放....已改为自动播放
            #browser.find_element_by_xpath("//div[@class='outter']").click()

            # 获取视频时长
            #video_duration_str = browser.find_element_by_class_name('duration').get_attribute('innerText')
            video_duration_str=autotextbyclass('duration',0)
            print('duration:'+video_duration_str)
            video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])
            print('视频时长:'+str(video_duration)+'秒,等待'+str(video_duration)+'秒')
            time.sleep(video_duration)
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
        autoclick(title, 0)
        windows = browser.window_handles
        browser.switch_to.window(windows[-1])
        for i in range(0, 2000, 100):

            js_code = "var q=document.documentElement.scrollTop=" + str(i)

            browser.execute_script(js_code)

            time.sleep(1)

        for i in range(2000, 0, -100):

            js_code = "var q=document.documentElement.scrollTop=" + str(i)

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

    time.sleep(2)

    gross_score = browser.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]")\

    get_attribute('innerText')

    today_score = browser.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')

    print("当前总积分：" + str(gross_score))

    print("今日积分：" + str(today_score))

    print("获取积分完毕，即将退出\n")


def waitlogin(printflag):

    printflag=True
    ##登陆后会跳转到一个URL可以用来判断是否完成登陆
    while(browser.current_url!=MY_STUDY):
        if(printflag):
            print('请使用手机强国学习APP扫描登陆')
            printflag=False
        time.sleep(1)
    print('用户已登陆')



if __name__ == '__main__':

    # 模拟登录
    login_simulation()

    # 阅读文章
    read_articles()

    # 观看视频
    watch_videos2()

    # 获得今日积分
    get_scores()

    browser.quit()
