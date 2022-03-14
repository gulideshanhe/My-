import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from PIL import Image, ImageDraw, ImageFont  # pip install pillow
wd = webdriver.Edge()
desktop = os.path.join(os.path.expanduser("~"), 'Desktop')  # 获取桌面路径


def screenshot():
	wd.maximize_window()
	wd.switch_to.default_content()
	time.sleep(1)
	wd.find_element(By.CSS_SELECTOR, '.lB2').screenshot(f'{desktop}\\0.png')
	wd.back()
	record = wd.find_element(By.CSS_SELECTOR, '.cha')
	record.click()
	wd.save_screenshot(f'{desktop}\\1.png')
	wd.quit()


def word(date):
	img1 = Image.open(f"{desktop}\\0.png")
	img2 = Image.open(f"{desktop}\\1.png")
	w2, h2 = img2.size
	w0, h0 = img1.size
	# x = location['x']
	# y = location['y']
	# w1 = size['width']
	# h1 = size['height']
	'''获取图片的位置和大小参数，但是似乎并不准确'''
	# img1 = img1.crop((x, y, (x+w1)*2, h0))  # 截取完成之后的图片
	img1 = img1.resize((w0*2, h2))
	result = Image.new('RGBA', (w0+w2, h2))
	result.paste(img2, box = (0, 0))
	result.paste(img1, box = (0, 0))
	# result.save("finish.png")
	'''加入字体'''
	draw = ImageDraw.Draw(result)
	ttfront = ImageFont.truetype('msyh.ttc', 120)  # 字体，大小
	content = ' '  # 需要加入图片的文字
	draw.text((w2/2, 20), content, fill = (0, 25, 25), font = ttfront)  # 文字位置，正文内容，文字RGB颜色，字体
	result.save(f'{desktop}\\{date}.png')
	# print('执行完毕')


def bf():
	# location = iframe.location  # 得到第一张图片的位置
	# # print(location)
	# size = iframe.size  # 得到第一章图片的大小
	# # print(size)
	wd.switch_to.frame(wd.find_element(By.CSS_SELECTOR, 'iframe'))  # 切换到播放窗口
	# 创建Select对象
	select = Select(wd.find_element(By.CSS_SELECTOR, "select[id=province]"))
	select.select_by_value("")  # 选择要求的省份
	city = Select(wd.find_element(By.CSS_SELECTOR, "select[id=city]"))
	city.select_by_value("")   # 选择要求的城市
	sure = wd.find_element(By.CSS_SELECTOR, '.sure')
	sure.click()
	time.sleep(3)  # 等待3秒加载动画
	start = wd.find_element(By.CSS_SELECTOR, '.start_btn')
	start.click()
	js = 'document.querySelector(".section3").className = "section3 topindex1"'
	wd.execute_script(js)  # 用于执行js代码，以跳过播放界面
	screenshot()


def date(day):
	today = time.strftime("%Y-%m-%d", time.localtime())
	if today == day:  # 用于判断日期是否是当天最新一期
		bf()  # 开始播放
		word(today)  # 加入文字
		os.remove(f'{desktop}\\1.png')
		os.remove(f'{desktop}\\0.png')
		'''最后删除其他图片文件'''
	else:
		wd.quit()


def sign():
	wd.get('http://home.yngqt.org.cn/qndxx/index.aspx')
	wd.implicitly_wait(10)
	''' 密码登录法,cookie登录实践失败'''
	signing = wd.find_element(By.CSS_SELECTOR, '.tan-login2')
	signing.click()
	username = wd.find_element(By.CSS_SELECTOR, '#login_username')
	username.send_keys('')  # 账号
	password = wd.find_element(By.CSS_SELECTOR, '#login_password')
	password.send_keys('')  # 密码
	sure = wd.find_element(By.CSS_SELECTOR, '.jiao[id=login_btn]')
	sure.click()
	sure = wd.find_element(By.CSS_SELECTOR, '.layui-layer-btn0')
	sure.click()
	study = wd.find_element(By.CSS_SELECTOR, '.yonghu1')
	study.click()
	day = wd.find_element(By.CSS_SELECTOR, 'h6')
	date(day.text[5:15])


if __name__ == '__main__':
	sign()
