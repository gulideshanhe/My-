class People:
	def __init__(self, money):
		self.money = money

	def add(self, number):
		self.money = self.money + number

	def subtract(self, number):
		if self.money - number < 0:
			print("余额不足,扣款失败")
		else:
			self.money = self.money - number

	def settlement(self):
		print(self.money)


def cot(who):
	if who:
		try:
			match commend[1]:
				case "s":
					who.subtract(int(commend[2:]))
					print("*"*5, f"{commend[0]}扣款{commend[2:]}")
					if com[1]:
						ret(com[1]).add(int(commend[2:]))
						print("*"*5, f"{com[1]}加{commend[2:]}")
				case "a":
					who.add(int(commend[2:]))
					print("*"*5, f"{commend[0]}加{commend[2:]}")
					# if com[1]:
					# 	ret(com[1]).subtract(int(commend[2:]))
				case out:
					print("*"*5, "输入有误，请重新输入")
		except ValueError:
			print("输入有误，请重新输入")


def ret(number):
	match number:
		case "1":
			return one
		case "2":
			return two
		case "3":
			return three
		case "4":
			return four
		case "5":
			return five
		case "s":
			one.settlement()
			two.settlement()
			three.settlement()
			four.settlement()
			five.settlement()
		case out:
			print("*"*5, "输入有误，请重新输入")


begin = int(input("输入初始金额："))
one = People(begin)
two = People(begin)
three = People(begin)
four = People(begin)
five = People(begin)
while True:
	com = input()
	com = com.replace(" ", "")
	com = com.split("t")
	commend = com[0]
	com.append("")
	try:
		cot(ret(commend[0]))
	except IndexError:
		print("输入有误，请重新输入")




