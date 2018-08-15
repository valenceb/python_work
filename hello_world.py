import json
import winsound  

# acctinfo = []
# acctinfo.append("asdf@sina.com")
# acctinfo.append("asdf")
filename = 'conf/account.json'

# with open(filename, 'w') as f_obj:
# 	json.dump(acctinfo, f_obj)

with open(filename) as f_obj:
	un = json.load(f_obj)

print(str(un))
winsound.Beep(600,1000)
