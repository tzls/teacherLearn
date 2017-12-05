# #test是对一些不确定的方法的调用做测试
# # from selenium import webdriver
# # from bs4 import  BeautifulSoup
# # driver = webdriver.Chrome()
# # driver.get("https://www.baidu.com/")
# # # if   driver.find_element_by_xpath("//table[@class = 'ui_border ui_state_visible ui_state_focus ui_state_lock']"):
# # #     print("正常的")
# # page_source = driver.page_source
# # soup = BeautifulSoup(page_source, 'lxml')
# # progressbar = soup.find("h5", attrs={"id": "div_ProgressBar_value"})
# # if not progressbar:
# #     print("为空")
# # print("hello")
# from configparser import ConfigParser
#
# cf = ConfigParser()
# cf.read("account.ini")
# print(cf.get("account","username"))
#
# str = '[单选]请计算：14+14=?\nA 28\nB 94\nC 123'
# strs = str.split('\n')
#
# index1 = strs[0].find('：')
# index2 = strs[0].find('+')
# index3 = strs[0].find('=')
# result1 = int(strs[1][2:len(strs[1])])
# result2 = int(strs[2][2:len(strs[2])])
# result3 = int(strs[3][2:len(strs[3])])
# result = int(strs[0][index1+1:index2])+int(strs[0][index2+1:index3])
# if (result == result1):
#     print("1")
# elif(result == result2):
#     print("2")
# elif(result== result3):
#     print("3")
# else:
#     print("4")
a = [1,2,3]
b = [4,5,6]
c = [7,8,9]
# a.append(b)
# b.extend(c)
a += b
print(a)
print(b)