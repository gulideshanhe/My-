import os
import time

import requests
from bs4 import BeautifulSoup


def study_sign():
	ss = requests.session()  # 可以记录cookie
	headers = {
		'user-agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
	}
	parms = '{"txtusername": "", "txtpassword": ""}'   # 登录时用的表单
	# 密码为明文的MD5
	resp = ss.post(url = "http://home.yngqt.org.cn/qndxx/login.ashx", data = parms, headers = headers)
	print(resp.text)
	# url = "https://home.yngqt.org.cn/qndxx/user/qiandao.ashx"  # 提交打卡的地址
	# take_study_card = ss.post(url, headers = headers)
	# print(take_study_card.text)
	if time.strftime("%A", time.localtime()) == "Monday":
		post_study_url = "http://home.yngqt.org.cn/qndxx/existsuser.ashx"  # 获取最新一期青年大学习的网址
		post_study_url_prarms = '{"user":"1"}'  # 获取网址时提交的表单信息
		study_url = ss.post(url = post_study_url, data = post_study_url_prarms, headers = headers)  # 请求学习地址
		the_study_url = study_url.json()["url"].replace("/index.html", "").replace(
			"https://h5.cyol.com/special/daxuexi/", "")  # 拿到学习网址
		title_url = f"https://h5.cyol.com/special/daxuexi/{the_study_url}/index.html"
		title = ss.get(url = title_url, headers = headers)
		soup = BeautifulSoup(title.content, 'html.parser')  # beautifulsoup分析网页，提取文字
		information = soup.select("h1")[0].text
		year = information[-9:-5]
		qi = information[-3:-1]
		study_or_not_url = "http://home.yngqt.org.cn/qndxx/xuexi.ashx"  # 是否已经学习
		post_study_url_prarms = '{txtid:' \
		                        f'{int(qi) + 100}' \
		                        '} '  # 提交内容为总期数，明年应该会有所改动，试试应该可以从别的地方获取
		study_or_not = ss.post(url = study_or_not_url, data = post_study_url_prarms, headers = headers)
		if study_or_not.json()["message"] == "您已学习过该期视频,确认需要再学习吗？":
			return
		else:
			finish_photo_url = f"https://h5.cyol.com/special/daxuexi/{the_study_url}/images/end.jpg"  # 拿到图片网址
			finish_photo = ss.get(url = finish_photo_url, headers = headers)  # 请求图片
			desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
			with open(f'{desktop}\\{time.strftime("%Y-%m-%d", time.localtime())}.png', 'wb') as f:
				f.write(finish_photo.content)  # 保存图片
			post_study_url = "https://gqti.zzdtec.com/api/event"  # 提交开始学习的网址
			study_time = int(time.time() * 1000)
			post_study_pramas = '{"guid":"e3eac9a1-dc76-822f-3a31-f90953443299","tc":"1655091883171",' \
			                    f'"tn":"{study_time}",' \
			                    f'"n":"开始学习","u":"https://h5.cyol.com/special/daxuexi/{the_study_url}/m.html?t=1&z=201",' \
			                    '"d":"cyol.com",' \
			                    f'"r":"https://h5.cyol.com/special/daxuexi/{the_study_url}/index.html","w":448,' \
			                    r'"m":"[{' \
			                    fr'\"c\":\"{year}\",\"s\":\"{qi}\",\"prov\":\"25\",\"city\":\"1\"' \
			                    r'}]"}'.encode("utf-8")
			begin_study = ss.post(url = post_study_url, data = post_study_pramas, headers = headers)
			print(begin_study.text, "学习完成！")


study_sign()
input()
