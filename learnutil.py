import threading
from bs4 import  BeautifulSoup
from selenium import webdriver
import selenium.common.exceptions
from utils.music.musicTest import *
from utils.spider.project_spider import *
from configparser import ConfigParser
from datetime import datetime

class Utils(object):
    def __init__(self):
        self.music = Music()
        self.driver = self.initDriver()
        self.first = True

    def initDriver(self):
        driver = webdriver.Chrome()
        cf = ConfigParser()
        cf.read("account.ini")
        driver.get("http://zjpx.hnhhlearning.com/")
        close_float_ad = driver.find_element_by_id("close_float_ad")
        close_float_ad.click()
        close_button = driver.find_elements_by_xpath("//input[@value='关闭']")[0]
        close_button.click()
        account = driver.find_element_by_xpath("//input[@id='LoginAccount']")
        account.send_keys(cf.get("account", "username"))
        password = driver.find_element_by_xpath("//input[@id='LoginPassword']")
        password.send_keys(cf.get("account", "password"))
        time.sleep(5)
        btn_submit = driver.find_element_by_xpath("//input[@id='btnSubmit1']")
        btn_submit.click()
        time.sleep(2)
        return driver

    def test(self):
        video_hrefs = ProjectSpider().spider(self.driver)
        print("video的数量...",len(video_hrefs))
        for video_href in video_hrefs:
            path = "http://zjxy.hnhhlearning.com/Study/Learning/MediaLi?sscId=%s"%(video_href)
            print("path..",path)
            self.watchVideo(path)
        print("恭喜！所有课程都学完了！！！")
    #暂时的设计思路是每5分钟查询一次当前进度，如果当前进度为100%，则return
    def watchVideo(self,path):
        self.driver.get(path)
        time.sleep(8)
        while(True):
            try :
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source,'lxml')
                progressbar = soup.find("h5",attrs={"id":"div_ProgressBar_value"}).get_text()
                #progressbar = driver.find_element_by_id("div_ProgressBar_value").text
                proprogressNum,sleepTime = self.getSleepTime(progressbar)
                #如果还未点击一次弹出框，则休眠5s
                if self.first:
                    sleepTime = 5
                #得到下次获取进度条的间隔时间
                print("progressbar..",progressbar,"..time..",sleepTime)
                #说明本节已经学完了
                if proprogressNum == 100:
                    print('本节已经学完')
                    return
                if self.wheClick(soup):
                    self.clickAnswer()
                    self.first = False
                #休息sleepTime后继续try
                print('睡前时间',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                time.sleep(sleepTime)
                print("睡后时间",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            except Exception as err:
                print("Exception",err)
                time.sleep(2)

    def process_end(self):
        for i in range(20):
            time.sleep(60)
            thread = threading.Thread(target=utils.endAction())
            thread.start()
    def getAnswer(self,ui_content):
        strs = ui_content.split('\n')
        index1 = strs[0].find('：')
        index2 = strs[0].find('+')
        index3 = strs[0].find('=')
        result1 = int(strs[1][2:len(strs[1])])
        result2 = int(strs[2][2:len(strs[2])])
        result3 = int(strs[3][2:len(strs[3])])
        result = int(strs[0][index1 + 1:index2]) + int(strs[0][index2 + 1:index3])
        #print("result1..",result1,"result2..",result2,"result3..",result3,"result..",result)
        if (result == result1):
           return 1
        elif (result == result2):
           return 2
        else:
           return 3
    def endAction(self):
        # 进度条
        div_ProgressBar_value = self.driver.find_element_by_id("div_ProgressBar_value").get_text()
        if div_ProgressBar_value == "100%":
            self.music.play()
    def click(self, radio, but_Question):
        path = '//input[@class=\'' + radio + '\']'
        print( )
        input = self.driver.find_elements_by_xpath("//input[@class='radio_A']")
        input.click()
        but_Question.click()
        time.sleep(2)
        if self.driver.find_elements_by_xpath("//input[@class='ui_state_highlight']"):
            button_sure = self.driver.find_elements_by_xpath("//input[@class='ui_state_highlight']")
            button_sure.click()
            return False
        else:
            return True
        #http://zjxy.hnhhlearning.com/Study/Learning/MediaLi?sscId=0ad46a54a73942f1abe084516b3df503&medId=a6c36e83331c492885b62eec6f9851e2
    #根据当前进度判断间隔时间，间隔多久再次获取进度
    def getSleepTime(self,progressbar):
        progressNum = int(progressbar[0:len(progressbar)-1])
        print("progressNum.",progressNum)
        if progressNum == 100:
            sleepTime = 0
        elif progressNum < 80:
            sleepTime = 598
        elif progressNum>90:
            sleepTime = 30
        else:
            sleepTime = 120
        return progressNum,sleepTime
    def wheClick(self,soup):
        #弹出的计算框的class属性有两种，两种任选一种均可视为有弹出计算框
        #ui_border ui_state_visible ui_state_focus ui_state_lock
        clock_window1 = soup.find("table",attrs={'class':'ui_border ui_state_visible ui_state_focus ui_state_lock'})
        clock_window2 = soup.find("table",attrs={'class':'ui_border ui_state_visible ui_state_lock ui_state_focus'})
        print("clock_window1..",clock_window1 is None,"clock_window2..",clock_window2 is None)
        if clock_window1 or clock_window2:
            return True
        else:
            return False

    def clickAnswer(self):
        #ui_border ui_state_visible ui_state_lock ui_state_focus
        #driver.find_element_by_xpath("//table[@class = 'ui_border ui_state_visible ui_state_focus ui_state_lock']")
        ui_content1 = self.driver.find_elements_by_xpath("//div[@class='ui_content']")
        print("答案1..", self.driver.find_element_by_xpath("//span[@id='divradio_A']").text)
        print("答案2..", self.driver.find_element_by_xpath("//span[@id='divradio_B']").text)
        print("答案3..", self.driver.find_element_by_xpath("//span[@id='divradio_C']").text)
        result1 = self.driver.find_element_by_xpath("//span[@id='divradio_A']")
        result2 = self.driver.find_element_by_xpath("//span[@id='divradio_B']")
        result3 = self.driver.find_element_by_xpath("//span[@id='divradio_C']")
        but_Question = self.driver.find_element_by_xpath("//input[@id='but_Question']")
        # 得到正确答案的序号
        index = self.getAnswer(ui_content1[0].text)
        print("clickk..答案", index)
        if index == 1:
            result1.click()
        elif index == 2:
            result2.click()
        else:
            result3.click()
        but_Question.click()

if __name__=='__main__':
    utils = Utils()
    utils.test()
    #div_ProgressBar_value
    # pro = Process(target=utils.process_end)
    # pro.start()
   # utils.test()


