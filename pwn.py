#!/usr/bin/python3
import requests
import json
import sys
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.web import JsonLexer



try:
	if sys.argv[1] == "--help" or sys.argv[1] == "-h":
		print("\t" +sys.argv[0] + " username 127.0.0.1:9050 - for username search  \n\t"+sys.argv[0]+" @example.com 127.0.0.1:9050 - for domain search")
		print("\t To install tor : sudo apt install tor\n\t To start the service : sudo service tor start")
		sys.exit(0)
except IndexError:
	print("\t" +sys.argv[0] + " username 127.0.0.1:9050 - for username search  \n\t"+sys.argv[0]+" @example.com 127.0.0.1:9050 - for domain search")
	print("\t To install tor : sudo apt install tor\n\t To start the service : sudo service tor start")
	sys.exit(0)



proxy = "127.0.0.1:9050"

try:
	if sys.argv[2]:
		proxy = sys.argv[2]
except:
	pass

leaked_users=[]
leaked_password=[]

if sys.argv[1]:
	userdomain = sys.argv[1]
	try:
		if userdomain.split("@"):
			username = userdomain.split("@")[0]
			domain = userdomain.split("@")[1]

	except:
		username = userdomain
		domain = ""
print("username : "+ username)
print("domain : " +domain)

url = "http://pwndb2am4tzkvold.onion/" 
#
session = requests.session()
session.proxies = {'http': 'socks5h://{}'.format(proxy), 'https': 'socks5h://{}'.format(proxy)}



data = {'luser': username, 'domain': domain, 'luseropr': 0, 'domainopr': 0, 'submitform': 'em'}

req = session.post(url, data=data)
detail = req.text
#print(req.text)

detail = detail.split("Array")[1:]

for leaks in detail:
	mail_leak = ''
	password = ''
	try :
	    mail_leak = leaks.split("[luser] =>")[1].split("[")[0].strip()
	    password = leaks.split("[password] =>")[1].split(")")[0].strip()

	except:
	    pass
	if mail_leak:
	    leaked_users.append({'Email': mail_leak+"@"+domain, 'Password' : password})
	    #leaked_password.append(password)

total_count=(len(leaked_users)-1)


print("\n[+] Proxy : " + proxy)
print()

for username in leaked_users[1:]:
	#print(json.dumps(username,indent=4))
	raw_json = json.dumps(username, indent=4)
	colorful = highlight(
	    raw_json,
	    lexer=JsonLexer(),
	    formatter=Terminal256Formatter(),
	)

	print(colorful)

print("[+] Number of users found in darkweb DB : " + str(total_count))
print()