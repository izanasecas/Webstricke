from pwn import *
import sys
import time
import string
import requests
import termcolor
import argparse
import signal
import os
from urllib.parse import urljoin, urlparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.basic_request import BasicRequestModule


# Control_C Function
def def_handler(sig, frame):
    print("\n\n[!] Saliendo del programa...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


class WebStrike:

    def __init__(self, url, user_agent, type_attack, quiet, method):
        
        self.url = url
        if user_agent:
            self.user_agent = user_agent
        else:
            self.user_agent= "WebStrike - Version:0.2"
        self.type_attack = type_attack
        self.session = requests.Session()
        if method:
            self.method = method
        else:
            self.method = "GET"

        if not quiet:
            self.banner()

        self.run()



    def banner(self):
        print("-------------------------------------------------")
        print("-                                               -")
        print("-                                               -")
        print("-                                               -")
        print("-                                               -")
        print("-              WebStrike                        -")
        print("-                                               -")
        print("- Dev by: @izanasecas                           -")
        print("- Version: 0.2                                  -")
        print("-                                               -")
        print("-------------------------------------------------")

        

    def checkurl(self ,url):

        if url.startswith(('http://', 'https://')):
            return True
        else:
            self.url = "http://"+url

        parsed = urlparse(self.url)
        if not parsed:
            print("\n[!] URL no inválida")
            sys.exit(1)

    def makesesion(self):
        # Configuración de sesión personalizada con cabeceras básicas
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'
        })

    def checkstatus(self):

        try:
            r = self.session.request(method=self.method, url=self.url, timeout=3)
            r.raise_for_status()
            if r.status_code == 200 or r.status_code == 302:
                return r.status_code

        except requests.exceptions.ConnectionError as err:
            print(f"Hemos tenido un error -> %s" % err.args[0])
            sys.exit(1)

        except requests.exceptions.HTTPError as err:
           print(f"Hemos tenido un error -> %s" % err.args[0])
           sys.exit(1)


    def load_module(self):

        ta_whitelist = ['Basic', 'SQLi', 'LFI', 'Regex', 'Match']
        module_mapping= {
            'Basic': BasicRequestModule
        }

        if self.type_attack not in ta_whitelist:
            print(f"\n[!] El modo de ataque especificado no es válido: -> %s" % self.type_attack)
            print(f"\n[!] Pruebe uno válido{ta_whitelist}")
            sys.exit(1)
        else:
            return module_mapping[self.type_attack]


    def run(self):
        print("\n[+] Iniciando el proceso")

        if self.checkurl(str(self.url)): # type: ignore
            pass
        print(f"URL objtetivo: %s" % self.url)
        print(f"User-Agent: %s" % self.user_agent)
        self.makesesion()
        print(f"Método para la petición: %s" % self.method)
        status_code = self.checkstatus()
        print(f"CheckStatus: Success(%s)" % status_code)
        print(f"Attack Mode: %s" % self.type_attack)
        print(f"------------------------------------------------")
        module_class = self.load_module()
        if module_class:
            module_instance =module_class(target_url=self.url, method=self.method, session=self.session)
        else:
            None 


def main():
    parser = argparse.ArgumentParser(description="WebStrike - Pentesting web, bug bounty")
    parser.add_argument('-u', '--url', required=True, help="Target URL to attack")
    parser.add_argument('-U', '--user-agent', help="Specific User-Agent")
    parser.add_argument('-t', '--type-attack',help="Type Attack that you want run (SQL, Regex, STTi,...)")
    parser.add_argument('-q', '--quiet', action="store_true", help="Quiet mode(without banner)")
    parser.add_argument('-m', '--method', help="Method of the Requests (GET, POST, PUT...)")

    args = parser.parse_args()

    webstricke = WebStrike(args.url, args.user_agent, args.type_attack, args.quiet, args.method)


if __name__ == '__main__':
    main()