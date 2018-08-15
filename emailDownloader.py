import json
import poplib
from email.parser import Parser
import base64

def get_details(msg):
    details = {}

    fromstr = msg.get('From')
    fromstr = decode_base64(fromstr.split("?")[3], charset=fromstr.split("?")[1])
    print("From:\n",fromstr)

    tostr = msg.get('To')

    subject = msg.get('Subject')
    subject = decode_base64(subject.split("?")[3], charset=subject.split("?")[1])
    print("Subject:\n", subject)

    received_time = msg.get("Date")
    print("Received Time:\n", received_time)

    parts = msg.get_payload()
    # content_type = parts[1].get_content_type()
    # content_charset = parts[1].get_content_charset()
    # content = parts[1].as_string().split('base64')[-1]
    content = str(parts)
    print('Content:\n', content)

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

	server = poplib.POP3(pop3_server)
	server.set_debuglevel(1)
	print(server.getwelcome().decode('utf8'))
	server.user(userName)
	server.pass_(pwd)
    
	resp, mails, octets = server.list()
	print('Total number of emails: {}'.format(len(mails)))
	total_mail_numbers = len(mails)
	response_status, mail_message_lines, octets = server.retr(total_mail_numbers)
	print('Email Status: {}'.format(response_status))
	print('This Emails bytes: {}'.format(octets))
	msg_content = b'\r\n'.join(mail_message_lines).decode('utf8')
	msg = Parser().parsestr(text=msg_content)
	server.close()
	return msg

if __name__ == '__main__':
	received_time = ""
	msg = get_parsed_msg()
	get_details(msg)
