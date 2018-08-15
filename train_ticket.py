from splinter.browser import Browser
import time
import winsound  

b = Browser(driver_name="firefox")
b.visit("https://kyfw.12306.cn/otn/index/init")
b.find_by_text("登录").click()
b.fill("loginUserDTO.user_name","valence.bai@qq.com")
b.fill("userDTO.password","bearsugar_1983")
b.find_by_text("客运首页").click()
b.cookies.add({"_jc_save_fromStation":"%u53A6%u95E8%2CXMS"})
b.cookies.add({"_jc_save_fromDate":"2018-02-17"})
b.cookies.add({"_jc_save_toStation":"%u5C24%u6EAA%2CYXS"})
b.reload()
button = b.find_by_id("a_search_ticket")
button.click()
print(b.find_by_id("ZE_5n000D65240K").text)
while True:
	if b.find_by_id("ZE_5n000D65240K").text != "无":
		button=b.find_by_text("预订")[2].click()
		winsound.Beep(600,1000)
		break
	else:
		b.find_by_text("查询").click()
		winsound.PlaySound('ALARM8', winsound.SND_ASYNC) 
		time.sleep(3)
