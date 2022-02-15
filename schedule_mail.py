#!/usr/bin/env python3

# coding: utf-8

import yagmail, os, requests, datetime, schedule, json, time, logging

class OneDayInfo():
    def __init__(self, filename, city_code, mail_receiver, personal_contents):
        self.filename = filename
        self.city_code = city_code
        self.mail_receiver = mail_receiver
        self.personal_contents = personal_contents
        self._today = datetime.date.today().isoformat()
    
    def logging_out(self, exec_error):
        logging.basicConfig(level=logging.DEBUG,
                            filename="/home/android/desktop/schedule_mail/schedule_mail_error.log",
                            format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
        logging.exception(exec_error)
        
    def get_mailposter_info(self):
        '''
        :filename: filename including mail poster information
        '''
        with open(self.filename, 'rb') as f:
            mailinfo = f.readlines()
        return [info.strip().decode() for info in mailinfo]

    def get_weather_info(self):
        '''
        :city_code: code of city to search
        '''
        url = "https://devapi.qweather.com/v7/weather/3d?location=%s&key=503f78630621427086cf1f77f612f2f9" % city_code
        resp = requests.get(url)
        threedays_weather_info_resp = resp.content.decode('utf-8')
        threedays_weather_info = json.loads(threedays_weather_info_resp)['daily']
        weather_info = '北京天气预报:\n'
        for i in threedays_weather_info:
            weather_info += i['fxDate'] + ", 最高温: " + i['tempMax'] + "℃, 最低温: " + i['tempMin'] + "℃, 白天天气: " + i['textDay'] + ", 晚间天气: " + i['textNight'] + ", 白天风力: " + i['windScaleDay'] + "级, 晚上风力: " + i['windScaleNight'] + "级\n"	

        return weather_info

    def get_youdao_oneday_words(self):
        yd_url = "https://dict.youdao.com/infoline?mode=publish&date=" + self._today + "&update=auto&apiversion=5.0"
        for record in requests.get(yd_url).json()[self._today]:
            if record['type'] == '壹句':
                oneday_words = "有道时间: " + self._today + ", 每日一句: " + record['title'] + ", 翻译: " + record['summary']
                break
        return oneday_words

    def get_shanbei_oneday_words(self):
        sb_url = "https://apiv3.shanbay.com/weapps/dailyquote/quote/?date=" + self._today
        record = requests.get(sb_url).json()
        oneday_words = "扇贝时间: " + self._today + ", 每日一句: " + record['content'] + ", 翻译: " + record['translation']
        return oneday_words

    def get_loving_words(self):
        loving_url_1 = "https://api.xygeng.cn/one"
        loving_url_2 = "https://res.abeim.cn/api-text_sweet?export=json"
        loving_url_3 = "https://api.ixiaowai.cn/api/ylapi.php"
        try:
            resp = requests.get(loving_url_1)
            loving_words_resp = resp.content.decode('utf-8')
            loving_words = json.loads(loving_words_resp)['data']['tag'] + ", " + json.loads(loving_words)['data']['origin'] + ", " +  json.loads(loving_words)['data']['content']
        except Exception:
            resp = requests.get(loving_url_2)
            loving_words_resp = resp.content.decode('utf-8')
            loving_words = json.loads(loving_words_resp)['content']
        except Exception:
            resp = requests.get(loving_url_3)
            loving_words = resp.content.decode('utf-8')

        return loving_words

    def get_weibo_hot(self):
        url = "https://tenapi.cn/resou/"
        resp = requests.get(url)
        weibo_hots_resp = resp.content.decode('utf-8')
        weibo_hots = json.loads(weibo_hots_resp)['list']
        weibo_hots_contents = ''
        for i in weibo_hots:
            weibo_hots_contents += "<a href=" + i['url'] + ">" + i['name'] + "</a>, 热搜指数: " + str(i['hot']) + "\n"
        return weibo_hots_contents

    def get_zhihu_hot(self):
        url = "https://tenapi.cn/zhihuresou/"
        resp = requests.get(url)
        weibo_hots_resp = resp.content.decode('utf-8')
        weibo_hots = json.loads(weibo_hots_resp)['list']
        weibo_hots_contents = ''
        for i in weibo_hots:
            weibo_hots_contents += "<a href=" + i['url'] + ">" + i['name'] + "</a>, 索引: " + str(i['query']) + "\n"
        return weibo_hots_contents

    def personal_words_for_my_wife(self):
        personal_words = self.personal_contents + '\n'
        return personal_words


    def send_oneday_contents(self, contents):
        mailinfo = self.get_mailposter_info()
        yag = yagmail.SMTP(mailinfo[0], mailinfo[1], host = 'smtp.163.com')
        yag.send(self.mail_receiver, "娇娇小可爱的每日提醒", contents=contents)
        self.logging_out("Mail-to-%s, 邮件已发送成功!" % self.mail_receiver)



filename = "/home/android/desktop/schedule_mail/.schedule_mailsetting"
city_code = "101010700"
mail_receiver = ["1724301832@qq.com", "2470687597@qq.com"]

if __name__ == "__main__":
    onedayinfo = OneDayInfo(filename=filename, city_code=city_code, mail_receiver=mail_receiver, personal_contents="🥰老婆，记得吃维C片, 两片呦🥰")
    try:
        weibo_hots = onedayinfo.get_weibo_hot()
        zhihu_hots = onedayinfo.get_zhihu_hot()
        personal_words_for_my_wife = onedayinfo.personal_words_for_my_wife()
        loving_words = onedayinfo.get_loving_words()
        oneday_words = onedayinfo.get_youdao_oneday_words() + "\n" + onedayinfo.get_shanbei_oneday_words()
        weather_info = onedayinfo.get_weather_info()

        schedule.every().day.at("07:30").do(onedayinfo.send_oneday_contents, weather_info)
        schedule.every().day.at("07:50").do(onedayinfo.send_oneday_contents, zhihu_hots)
        schedule.every().day.at("09:30").do(onedayinfo.send_oneday_contents, weibo_hots)
        schedule.every().day.at("09:40").do(onedayinfo.send_oneday_contents, oneday_words)
        schedule.every().day.at("22:30").do(onedayinfo.send_oneday_contents, personal_words_for_my_wife)
        schedule.every().day.at("23:20").do(onedayinfo.send_oneday_contents, weather_info)
        schedule.every().day.at("23:30").do(onedayinfo.send_oneday_contents, loving_words)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        onedayinfo.logging_out(e)

        
        
