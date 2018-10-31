from db import settings
from pymongo import MongoClient 
from datetime import datetime
from datetime import timedelta
class VideoAnalyzer(object):
    def __init__(self):
        # 链接mongoDB
        self.client = MongoClient(settings['MINGO_HOST'], 27017)
        # 数据库登录需要帐号密码
        self.client.admin.authenticate(settings['MINGO_USER'],
                                        settings['MONGO_PSW'])
        self.db = self.client['biliob']  # 获得数据库的句柄
        self.coll = self.db['video']  # 获得collection的句柄
    def video_filter(self):
        pre_view = -1
        c_view = -1
        delta = timedelta(1)
        pre_date = datetime
        c_date = datetime
        count_delete = 0
        count_unfocus = 0
        count_focus = 0
        for each_doc in self.coll.find({'focus':True}):
            live_time = 0
            delete = False
            focus = True
            if 'data' in each_doc:
                each_doc['data'].reverse()
                for each_data in each_doc['data']:
                    
                    if pre_view == -1:
                        pre_view = each_data['view']
                        pre_date = each_data['datetime']
                        continue
                    c_view = each_data['view']
                    c_date = each_data['datetime']

                    if pre_date + delta > c_date:
                        continue
                    live_time +=1
                    rate = (c_view-pre_view)
                    pre_view = c_view
                    pre_date = c_date

                    if live_time == 3 and c_view < 3000:
                        delete = True
                        focus = False
                        break
                    elif live_time > 3 and rate < 100:
                        focus = False
                        delete = False
                        break
                    else:
                        focus = True
                        delete = False
                if delete:
                    count_delete += 1
                    print("! 删除追踪："+each_doc['title']+' 当前播放：'+str(each_doc['data'][len(each_doc['data'])-1]['view']))
                    self.coll.delete_one({'aid':each_doc['aid']})
                elif focus:
                    count_focus += 1
                    print("√ 持续追踪："+each_doc['title']+' 当前播放：'+str(each_doc['data'][len(each_doc['data'])-1]['view']))
                else:
                    count_unfocus += 1
                    print("× 不再追踪："+each_doc['title']+' 当前播放：'+str(each_doc['data'][len(each_doc['data'])-1]['view']))
                    self.coll.update_one({'aid':each_doc['aid']},{'$set':{'focus':False}})
                pre_view = -1
                c_view = -1
        print("· 本轮筛选结果：")
        print("! 删除辣鸡总数："+str(count_delete))
        print("× 不再追踪总数："+str(count_unfocus))
        print("√ 持续追踪总数："+str(count_focus))
    