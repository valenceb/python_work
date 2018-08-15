#coding=utf8
import json
import poplib
from email.parser import Parser
import base64

def get_details(msg):
    # ���������Ϣ���ֵ䣬���ڷ���
    details = {}

    # ��ȡ����������
    fromstr = msg.get('From')
    fromstr = decode_base64(fromstr.split("?")[3], charset=fromstr.split("?")[1])
    print("From:\n",fromstr)

    # ��ȡ�ռ�������
    tostr = msg.get('To')

    # ��ȡ������Ϣ��Ҳ���Ǳ�������
    subject = msg.get('Subject')
    subject = decode_base64(subject.split("?")[3], charset=subject.split("?")[1])
    print("Subject:\n", subject)

    # ��ȡʱ����Ϣ��Ҳ�����ʼ����������յ���ʱ��
    received_time = msg.get("Date")
    print("Received Time:\n", received_time)

    parts = msg.get_payload()
    # print('8'*9, parts[0].as_string())
    content_type = parts[0].get_content_type()
    content_charset = parts[0].get_content_charset()
    # parts[0] Ĭ��Ϊ�ı���Ϣ����parts[1]Ĭ��Ϊ�����HTML�����������Ϣ
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

    # ��ʼ���ӵ�������
	server = poplib.POP3(pop3_server)
    # ��ѡ� �򿪻��߹رյ�����Ϣ��1Ϊ�򿪣����ڿ���̨��ӡ�ͻ�����������Ľ�����Ϣ
	server.set_debuglevel(1)
    # ��ѡ� ��ӡPOP3�������Ļ�ӭ���֣���֤�Ƿ���ȷ���ӵ����ʼ�������
	print(server.getwelcome().decode('utf8'))
    # ��ʼ���������֤
	server.user(userName)
	server.pass_(pwd)
    
    # # �����ʼ�����Ŀ��ռ�÷������Ŀռ��С���ֽ������� ͨ��stat()��������
	# print("Mail counts: {0}, Storage Size: {0}".format(server.stat()))
	# # ʹ��list()���������ʼ��ı�ţ�Ĭ��Ϊ�ֽ����͵Ĵ�
	# resp, mails, octets = server.list()
	# print("��Ӧ��Ϣ�� ", resp)
	# print("�����ʼ���Ҫ��Ϣ�� ", mails)
	# print("list�����������ݴ�С���ֽڣ��� ", octets)
    
    # ʹ��list()���������ʼ��ı�ţ�Ĭ��Ϊ�ֽ����͵Ĵ�
	resp, mails, octets = server.list()
	print('�ʼ������� {}'.format(len(mails)))
    # ���浥����ȡ���µ�һ���ʼ�
	total_mail_numbers = len(mails)
    # Ĭ���±�Խ���ʼ�Խ�£�����total_mail_numbers�������µ��Ƿ��ʼ�
	response_status, mail_message_lines, octets = server.retr(total_mail_numbers)
	print('�ʼ���ȡ״̬�� {}'.format(response_status))
	#print('ԭʼ�ʼ�����:\n{}'.format(mail_message_lines))
	print('�÷��ʼ���ռ�ֽڴ�С: {}'.format(octets))
	msg_content = b'\r\n'.join(mail_message_lines).decode('gbk')
	# �ʼ�ԭʼ����û����������������Ҫ��Ӧ�Ľ��н������
	msg = Parser().parsestr(text=msg_content)
	#print('�������ʼ���Ϣ:\n{}'.format(msg))
    # �ر�������������ӣ��ͷ���Դ
	server.close()
	return msg

if __name__ == '__main__':
	received_time = ""
	msg = get_parsed_msg()
	get_details(msg)
