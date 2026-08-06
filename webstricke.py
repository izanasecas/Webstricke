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
from modules.directory_buster import DirectoryBusterModule

# Control_C Function
def def_handler(sig, frame):
    print("\n\n[!] Saliendo del programa...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


class WebStrike:

    def __init__(self, url, user_agent, type_attack, quiet, method, output=None, format='json', threads=10, wordlist=None):
        
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

        self.output = output    
        self.format = format
        self.threads = threads
        self.wordlist = wordlist

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
            r = self.session.request(method=self.method, url=self.url, timeout=10)
            r.raise_for_status()
            if r.status_code == 200 or r.status_code == 302:
                return r.status_code

        except requests.exceptions.ConnectionError as err:
            print(f"Hemos tenido un error -> %s" % err.args[0])
            sys.exit(1)

        except requests.exceptions.HTTPError as err:
           print(f"Hemos tenido un error -> %s" % err.args[0])
           sys.exit(1)
        except requests.exceptions.ReadTimeout:
            print(f"\n[!] Timeout: El servidor no responde en 10 segundos")
            print("[!] Prueba a aumentar el timeout o verifica que el servidor está activo")
            sys.exit(1)


    def load_module(self):

        ta_whitelist = ['Basic', 'SQLi', 'LFI', 'Regex', 'Match', 'DirBuster']
        module_mapping= {
            'Basic': BasicRequestModule,
            'DirBuster': DirectoryBusterModule
        }

        if self.type_attack not in ta_whitelist:
            print(f"\n[!] El modo de ataque especificado no es válido: -> %s" % self.type_attack)
            print(f"\n[!] Pruebe uno válido{ta_whitelist}")
            sys.exit(1)
        else:
            return module_mapping[self.type_attack]


    def export_results(self, results, module_name):
        # Módulo para la exportación de resultados

        if not self.output:
            return
        
        try:
            import json
            from datetime import datetime

            report_data = {
             "target": self.url,
             "method": self.method,
             "module": module_name,
             "timestamp": datetime.now().isoformat(),
             "results": results   
            }

            # Formato JSON
            if self.format == 'json':
                with open(self.output, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, default=str, ensure_ascii=False)
                print(f"\n[+] Resultados exportdos en {self.output} (JSON)")

            # Formato en TXT
            elif self.format == 'txt':
                with open(self.output, 'w', encoding='utf-8') as f:
                    f.write(f"WebStricke report\n")
                    f.write(f"{'='*50}\n")
                    f.write(f"Target: {self.url}\n")
                    f.write(f"Módulo: {module_name}\n")
                    f.write(f"Método: {self.method}\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"{'='*50}\n\n")

                    #Información básica
                    f.write(f"Status code: {results.get('status_code', 'N/A')}\n")
                    f.write(f"Response time: {results.get('response_time', 'N/A')}s\n")
                    f.write(f"URL Final: {results.get('final_url', 'N/A')}\n")

                    #Headers
                    if 'response_headers' in results:
                        f.write(f"\nHeaders:\n")
                        for key, value in results['response_headers'].items():
                            f.write(f"  {key}: {value}")
                    
                    # Security headers
                    if 'security_headers' in results:
                        f.write(f"\nSecurity Headers:\n")
                        for header, info in results['security_headers'].items():
                            value = info.get('value','')
                            status = info.get('status','UNKNOW')
                            f.write(f"  {header}: {status}")
                            if value:
                                f.write(f"({value})")
                            f.write(f"\n")
                    print(f"[+] Resultados exportados a: {self.output} (TXT)")
        except  Exception as e:
            print(f"[!] Error ocurrido exportando datos: {e}")



                    


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
            if self.type_attack == 'DirBuster':
                threads = getattr(self, 'threads', 10)
                module_instance =module_class(target_url=self.url, method=self.method, session=self.session, threads=threads, wordlist=self.wordlist)

            else:
                module_instance =module_class(target_url=self.url, method=self.method, session=self.session)
        
        if hasattr(module_instance, 'results'):
            self.scan_results = module_instance.results
            self.export_results(self.scan_results, self.type_attack) 


def main():
    parser = argparse.ArgumentParser(description="WebStrike - Pentesting web, bug bounty")
    parser.add_argument('-u', '--url', required=True, help="Target URL to attack")
    parser.add_argument('-U', '--user-agent', help="Specific User-Agent")
    parser.add_argument('-t', '--type-attack',help="Type Attack that you want run (SQL, Regex, STTi,...)")
    parser.add_argument('-q', '--quiet', action="store_true", help="Quiet mode(without banner)")
    parser.add_argument('-m', '--method', help="Method of the Requests (GET, POST, PUT...)")
    parser.add_argument('-o', '--output', help="Archivo de salida, sorporta(txt, json)")
    parser.add_argument('-f', '--format', choices=['json','txt'], default='json', help='Formato de salida (por defecto JSON)')
    parser.add_argument('-T', '--threads', type=int, default=10, help="Número de threads (para Dirbuster)")
    parser.add_argument('-w', '--wordlist', help="Wordlist personalizado (Para DirBuster)")

    args = parser.parse_args()

    webstricke = WebStrike(args.url, args.user_agent, args.type_attack, args.quiet, args.method, args.output, args.format, args.threads, args.wordlist)


if __name__ == '__main__':
    main()