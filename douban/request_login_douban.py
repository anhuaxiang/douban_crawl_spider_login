import urllib
import re
import cookielib
import EncodePostData
import webbrowser


class DouBan:
    def __init__(self, username, password):
        # 初始化登录地址、账号和密码
        self.loginUrl = "https://accounts.douban.com/login"
        self.username = username
        self.password = password
        self.cookies = cookielib.CookieJar()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Host': 'accounts.douban.com',
            'Referer': 'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '129'
        }

    # 登录程序
    def login(self):
        # self.EnableCookieAndProxy()   # 使用代理
        source, redir, yzmUrl, captchaID = self.getData()   # 返回相关post数据和验证码链接
        if yzmUrl:  # 如果有验证码
            captchaSolution = self.getCaptchSolution(yzmUrl)   # 获取验证码
            print(captchaSolution)
        else:
            captchaSolution = ""
        postData = EncodePostData.PostEncode(self.username, self.password, source, redir, captchaSolution, captchaID)
        request = urllib2.Request(self.loginUrl, postData, self.headers)
        response = urllib2.urlopen(self.loginUrl, postData)

    # 添加代理和cookie
    def EnableCookieAndProxy(self):
        # 添加cookie
        cookieSupport = urllib2.HTTPCookieProcessor(self.cookies)
        # 添加代理
        proxySupport = urllib2.ProxyHandler({'http': '58.222.254.11:3128'})  # 使用代理
        opener = urllib2.build_opener(proxySupport, cookieSupport, urllib2.HTTPHandler)
        urllib2.install_opener(opener)  # 构建对应的opener

    # 获取post数据和验证码链接
    def getData(self):
        page = urllib2.urlopen(self.loginUrl).read()
        # source, redir, captchaID, login, yzm
        pattern = re.compile('<input name="source".*?value="(.*?)".*?<input name="redir".*?value="(.*?)".*?<img id="captcha_image" src="(.*?)".*?<input.*?name="captcha-id" value="(.*?)"', re.S)
        items = re.search(pattern, page)
        print("captcha-id: ", items.group(4))
        #       source          redir           yzmUrl          captcha-id
        return items.group(1), items.group(2), items.group(3), items.group(4)

    # 读取验证码
    @classmethod
    def getCaptchSolution(cls, yzmUrl):
        webbrowser.open_new_tab(yzmUrl)  # 打开验证码图片
        # 手动输入验证码
        yzm = raw_input("请输入浏览器显示的验证码: ")
        return str(yzm)

# 测试代码
db = DouBan("这是账号", "这是密码")
db.login()
