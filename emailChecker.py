#coding=utf8
import json
import poplib
from email.parser import Parser
import base64

def get_details(msg):
    # 保存核心信息的字典，用于返回
    details = {}

    # 获取发件人详情
    fromstr = msg.get('From')
    fromstr = decode_base64(fromstr.split("?")[3], charset=fromstr.split("?")[1])
    print("From:\n",fromstr)

    # 获取收件人详情
    tostr = msg.get('To')

    # 获取主题信息，也就是标题内容
    subject = msg.get('Subject')
    subject = decode_base64(subject.split("?")[3], charset=subject.split("?")[1])
    print("Subject:\n", subject)

    # 获取时间信息，也即是邮件被服务器收到的时间
    received_time = msg.get("Date")
    print("Received Time:\n", received_time)

    parts = msg.get_payload()
    # print('8'*9, parts[0].as_string())
    content_type = parts[0].get_content_type()
    content_charset = parts[0].get_content_charset()
    # parts[0] 默认为文本信息，而parts[1]默认为添加了HTML代码的数据信息
    content = parts[0].as_string().split('base64')[-1]
    print('Content:\n', decode_base64(content, content_charset))
    # content = parts[1].as_string().split('base64')[-1]
    # print('HTML Content:', decode_base64(content, content_charset))

def decode_base64(s, charset='gbk'):
	return str(base64.decodebytes(s.encode(encoding=charset)), encoding=charset)

def get_parsed_msg():
	filename = 'conf/account.json'
	with open(filename) as f_obj:
		acct = json.load(f_obj)
	if len(acct)==2:
		userName = acct[0]
		pwd = acct[1]

	pop3_server = 'pop.sina.com'
	smtp_server = 'smtp.sina.com'

    # 开始连接到服务器
	server = poplib.POP3(pop3_server)
    # 可选项： 打开或者关闭调试信息，1为打开，会在控制台打印客户端与服务器的交互信息
	server.set_debuglevel(1)
    # 可选项： 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
	print(server.getwelcome().decode('utf8'))
    # 开始进行身份验证
	server.user(userName)
	server.pass_(pwd)
    
    # # 返回邮件总数目和占用服务器的空间大小（字节数）， 通过stat()方法即可
	# print("Mail counts: {0}, Storage Size: {0}".format(server.stat()))
	# # 使用list()返回所有邮件的编号，默认为字节类型的串
	# resp, mails, octets = server.list()
	# print("响应信息： ", resp)
	# print("所有邮件简要信息： ", mails)
	# print("list方法返回数据大小（字节）： ", octets)
    
    # 使用list()返回所有邮件的编号，默认为字节类型的串
	resp, mails, octets = server.list()
	print('邮件总数： {}'.format(len(mails)))
    # 下面单纯获取最新的一封邮件
	total_mail_numbers = len(mails)
    # 默认下标越大，邮件越新，所以total_mail_numbers代表最新的那封邮件
	response_status, mail_message_lines, octets = server.retr(total_mail_numbers)
	print('邮件获取状态： {}'.format(response_status))
	#print('原始邮件数据:\n{}'.format(mail_message_lines))
	print('该封邮件所占字节大小: {}'.format(octets))
	msg_content = b'\r\n'.join(mail_message_lines).decode('gbk')
	# 邮件原始数据没法正常浏览，因此需要相应的进行解码操作
	msg = Parser().parsestr(text=msg_content)
	#print('解码后的邮件信息:\n{}'.format(msg))
    # 关闭与服务器的连接，释放资源
	server.close()
	return msg

if __name__ == '__main__':
	received_time = ""
	msg = get_parsed_msg()
	get_details(msg)
