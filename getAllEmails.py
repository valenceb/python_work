# coding: gbk
import json
import poplib

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

# �����ʼ�����Ŀ��ռ�÷������Ŀռ��С���ֽ������� ͨ��stat()��������
print("Mail counts: {0}, Storage Size: {0}".format(server.stat()))
# ʹ��list()���������ʼ��ı�ţ�Ĭ��Ϊ�ֽ����͵Ĵ�
resp, mails, octets = server.list()
print("��Ӧ��Ϣ�� ", resp)
print("�����ʼ���Ҫ��Ϣ�� ", mails)
print("list�����������ݴ�С���ֽڣ��� ", octets)

# �ر�������������ӣ��ͷ���Դ
server.close()
