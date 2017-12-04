from  utils.learnutil import  *
import re
#爬取所有课程模块链接
class ProjectSpider:
     def spider(self,driver):
         self.driver = driver
         project_handled = self.spider_home("http://zjxy.hnhhlearning.com/Home","/Course/MyCourse/CourseStudy")
         video_hrefs = []
         for project in project_handled:
             print("二级页面id", project)
             path = 'http://zjxy.hnhhlearning.com/Study/Learning?sscId=%s' % (project)
             print("拼接出的二级界面地址...",path)
             project_hrefs= self.spider_home(path, "/Course/MyCourse/MediaStudy")
             print("视频页面地址..",project_hrefs)
             video_hrefs.extend(project_hrefs)
         return video_hrefs

     def spider_home(self,path,condition):
         self.driver.get(path)
         time.sleep(2)
         page_source = self.driver.page_source
         soup = BeautifulSoup(page_source, 'lxml')
         project_handled = []
         # 进度条列表
         process_lists = soup.find_all("embed")
         # 课程列表
         project_lists = soup.find_all(href=re.compile(condition))
         print("lists的大小...", len(process_lists), "列表的大小...", len(project_lists))
         if len(project_lists) != len(process_lists):
             print("进度条的数量和课程的数量不一致")
             return None
         for i in range(len(project_lists)):
             if self.getWhetProcess(process_lists[i].attrs["src"]):
                 project_handled.append(self.getSscid(project_lists[i].attrs['href']))
         return project_handled


     #处理获取的进度条信息，根据进度条来判断是否加入待处理
     def getWhetProcess(self,embed):
         # "http://res.gkwlpx.com/Domain/2/default/baifen.swf?id=100
         index = embed.find('=')
         num = int(embed[index + 1:len(embed)])
         print('embed...', embed, '..num.....', num)
         if num is 100:
             return False
         else:
             return True
    #根据获取的链接信息，获取二级页面Id
     def getSscid(self,href):
         if "&amp" not in href:
             print('href1...', href)
             index = href.find('=')
             project_id = href[index + 1:len(href)]
             print('href...', href, 'project_id....', project_id)
         else:
             print("href2...", href)
             index1 = href.find("=", 1)
             index2 = href.find("&")
             project_id = project_id = href[index1 + 1:index2]
             print('href...', href, 'project_id....', project_id)
         return project_id

if __name__=='__main__':
    ps = ProjectSpider()
    ps.spider()


