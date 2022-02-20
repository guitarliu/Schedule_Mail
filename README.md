## Schedule_Mail
定时邮件通知脚本，通知内容包括天气、热搜等内容

---
#### 一、功能

获取以下信息并定时发送至目标邮箱:

- ✔️ 获取天气信息;
- ✔️ 获取有道每日一词、扇贝每日一词;
- ✔️ 获取每日情话;
- ✔️ 获取每日微博热点;
- ✔️ 获取每日知乎热搜;
- ✔️ 自定义邮件内容(仅支持文字类);

#### 二、相关API
相关信息对应的API见下表:

|API名称|API链接|
|:--------------------:|:--------------------:|
|[和风天气](https://dev.qweather.com/docs/api/)|https://dev.qweather.com/docs/api/|
|有道每日一词|"https://dict.youdao.com/infoline?mode=publish&date=[datetime]&update=auto&apiversion=5.0|
|扇贝每日一词|https://apiv3.shanbay.com/weapps/dailyquote/quote/?date=[datetime]|
|每日情话|https://api.xygeng.cn/one|
|每日情话|https://res.abeim.cn/api-text_sweet?export=json|
|每日情话|https://api.ixiaowai.cn/api/ylapi.php|
|微博热点|https://tenapi.cn/resou/|
|知乎热搜|https://tenapi.cn/zhihuresou/|


***PS: 部分API存在无法访问的请况~~~.***

