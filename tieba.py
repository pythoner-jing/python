# coding:utf-8
# author:wishout
# date:2013/8/2
import re, urllib, urllib2, cookielib
import ConfigParser as cp

# 百度登陆页面url
loginUrl = "https://passport.baidu.com/v2/?login"
# 登陆url
postUrl = "https://passport.baidu.com/v2/api/?login"
# 回帖url
replyUrl = "http://tieba.baidu.com/f/commit/post/add"
# 签到url
signUrl = "http://tieba.baidu.com/sign/add"
# 设置cookie处理器，负责从服务器下载cookie，并在请求提交时附带cookie
cookie = cookielib.LWPCookieJar()
cookieProc = urllib2.HTTPCookieProcessor(cookie)
# 设置并安装url打开器
opener = urllib2.build_opener(cookieProc, urllib2.HTTPHandler)
urllib2.install_opener(opener)
# 开始下载cookie
socket = urllib2.urlopen(loginUrl)

# 过滤字段的正则式
tokenRegex = re.compile(r"login_token=\'(.+)\'")
kwRegex = re.compile(r"kw:\'(.+)\'")
fidRegex = re.compile(r"fid:\'(\d+)\'")
tidRegex = re.compile(r"tid:\'(\d+)\'")
tbsRegex = re.compile(r"\'tbs\'.+\"(.+)\"\,") 
favorRegex = re.compile(r"kw=([^&\s>\\]+)")
signTbsRegex = re.compile(r"PageData\.tbs\s=\s\"(.+)\"")
codeRegex = re.compile(r"no\":([^,]+)")

# 登陆所使用的请求头
loginHeader = {
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Content-Type":"application/x-www-form-urlencoded",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22", 
	"Referer" : "https://passport.baidu.com/v2/?login"
}

# token，username，password为关键字段，保留
loginData = {
	"charset":"UTF-8",
	"token":" ",
	"tpl":"pp",
	"isPhone":"false",
	"safeflg":"0",
	"u":"https://passport.baidu.com/",
	"username":"",
	"password":"",
	"mem_pass":"on"
}

# 签到请求头
signHeader = {
"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3",
"Accept-Language":"zh-CN,zh;q=0.8",
"Connection":"keep-alive",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22",
}

# 签到字段，kw，tbs为关键字段，保留
signData = {
"ie":"utf-8",
"kw":"0",
"tbs":"0"
}

# 登陆函数
def login(username, password):
	# 获取关键字段token
	request = urllib2.Request("https://passport.baidu.com/v2/api/?getapi&class=login&tpl=pp&tangram=false")
	page = opener.open(request).read().decode("utf-8")
	rs = tokenRegex.search(page)

	global loginData
	loginData["token"] = rs.group(1)
	loginData["username"] = username
	loginData["password"] = password

	loginData = urllib.urlencode(loginData)

	request = urllib2.Request(postUrl, loginData, loginHeader)
	response = urllib2.urlopen(request)
	page = response.read()
	
	# print page

	page = urllib2.urlopen("http://tieba.baidu.com").read()
	rs = re.findall("<li\s+class=\"u_itieba\"><div><a href=\"([^\"]+)", page)

	print "logined"

def sign(username):
	name = urllib.quote(username)
	page = urllib.urlopen("http://www.baidu.com/p/%s?from=tieba" % name).read()
	rs = favorRegex.findall(page)

	# 去重
	favorList = list(set(rs))
	kwList = []

	f = open("output.txt", "w")

	for i in favorList:
		kwList.append(i)
		f.write(urllib.unquote(i) + "\n")

	f.close()

	global signData
	for i in kwList:
		page = urllib2.urlopen("http://tieba.baidu.com/f?kw=" + i).read()
		tbs = signTbsRegex.search(page)

		signData["kw"] = urllib.unquote(i).decode("gbk").encode("utf-8")
		signData["tbs"] = tbs.group(1)

		print urllib.unquote(i)
		data = urllib.urlencode(signData)
		request = urllib2.Request(signUrl, data, signHeader)
		response = urllib2.urlopen(request)
		page = response.read()
		code = codeRegex.search(page).group(1)

		if code == "0" or code == "1101" or code == "1102":
			print "ok"
		elif code == "1010":
			print "error"
		elif code == "1100":
			print "busy"

	print "signed"

def main():
	config = cp.ConfigParser()
	config.read("login.ini")
	section = "tieba"
	data = {}

	for option in config.options(section):
		data[option] = config.get(section, option)

	login(data["username"], data["password"])
	sign(data["username"])

if __name__ == "__main__":
	main()
