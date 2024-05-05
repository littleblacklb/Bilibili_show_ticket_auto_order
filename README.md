# Bilibili_show_ticket_auto_order （小黑重写版）

**该项目在原有的基础上支持多用户抢票**

由于个人认为[原项目](https://github.com/fengx1a0/Bilibili_show_ticket_auto_order)的代码组织难以维护与更新，
于是我打算在保留原先程序的机制情况下对大部分代码进行重写，方便后续其他大佬的后续添加新功能及维护。

本人能力有限，所以如果您认为代码还是很烂请谅解 :~)

如果有代码中的任何不足之处，都可欢迎PR

## 本项目仅供Python、httpx、asyncio、pydantic、Selenium操作学习使用。

## 截止到 2024/4/23 仍然可用

<img width="273" alt="屏幕截图 2023-08-09 182035" src="https://github.com/fengx1a0/Bilibili_show_ticket_auto_order/assets/74698099/f0b2d1ad-928b-498d-9a79-f735e3f01c00">

<img width="277" alt="屏幕截图 2023-08-09 182012" src="https://github.com/fengx1a0/Bilibili_show_ticket_auto_order/assets/74698099/4363ff9a-23a7-4f31-b0ea-0919ed1279d1">

> 本软件承诺不包含任何个人信息采集与远程遥测组件，开发者不会远程对程序本身、账号以及账号所有者的任何信息进行任何恶意操作
>
> 本软件无法保证 100% 命中率和 100% 不受哔哩哔哩安全团队行为风险控制限制，一切交给天意
>
> 本软件可能无法及时跟进哔哩哔哩验证码机制更新，望知悉
>
> 本项目不会使用各种条款、“保密协议”等对使用者进行额外限制，代码明文可见，遵循GPL（GNU General Public License）协议进行开源。

# 原介绍

本项目核心借鉴自https://github.com/Hobr 佬

Bilibili会员购抢票助手, 通过B站接口抢购目标漫展/演出

本脚本仅供学习交流使用, 不得用于商业用途, 如有侵权请联系删除

<img src="images/image-20230708221711220.png" alt="image-20230708221711220" style="zoom:50%;" />

<img src="images/a.png" alt="image-20230708221143842" style="zoom:50%;" />

## 致谢

以下排名不分先后，我也不想搞的攀比起来，因为很多都是学生，原则上我是不收赞助的，大家太热情了：

------------------------------------------------++++

```
晚安乃琳Queen
kankele
倔强
宵宫
yxw
星海云梦
穆桉
mizore
傩祓
CChhdCC
w2768
iiiiimilet
利维坦战斧
路人
Impact
骤雨初歇
明月夜
晓读
Simpson
Goognaloli
闹钟
LhiaS
洛天华
猪猪侠
awasl
房Z
浙江大学第一深情
superset245
ChinoHao
神秘的miku
Red_uncle
czpwpq
```

------------------------------------------------++++

## 功能截图

除了登录纯api请求

目前已经支持漫展演出等的 无证 / 单证 / 一人一证 的购买

<img src="images/image-20230708014050624.png" alt="image-20230708014050624" style="zoom:50%;" />

<img src="images/image-20230708014124395.png" alt="image-20230708014124395" style="zoom:50%;" />

## 使用

相关内容感谢@123485k的提交

### 执行exe

登录和抢票分开的，先运行登录.exe，登陆后再运行抢票.exe，运行了之后不要急着选，先把验证.exe启动起来

不需要依赖

如果运行失败的请安装依赖[Edgewebdriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

### 执行脚本

请确保引用的库安装正常。

```shell
pip install -r requirements.txt
```

```shell
python login.py     //登录
python main.py      //抢票
python geetest.py   //极验滑块验证
```

### 新功能：微信公众号推送结果

需要关注pushplus微信公众号，关注后激活，然后点击个人中心-获取token，在config.txt中填入token即可在需要验证或者抢票成功后收到微信公众号通知

## 配置说明 及其 格式

```json
{
  "http": {
    // 每次抢票操作间隔时间
    "sleep": 1.7,
    // HTTP错误 重试操作间隔
    "retry_delay": 1,
    // HTTP错误 重试最大次数
    "retry_max_times": 3,
    // 代理 http 网站的 http代理设置 （为空则不代理）
    "proxy_http": "http://127.0.0.1:10801",
    // 代理 https 网站的 http代理设置（为空则不代理）
    "proxy_https": "http://127.0.0.1:10801"
  },
  "users": [
    {
      // 抢票用户uid
      "uid": 1145141224,
      // 展出项目id
      "project_id": 81122,
      // 身份证认证姓名
      "idcard_name": "卢本伟"
    },
    {
      "uid": 19198101224,
      "project_id": 2233,
      "idcard_name": "伞兵一号"
    }
    // ...
  ]
}
```

## 问题报告

提issue即可