import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Módulo para el descubrimiento de archivos y directorios

class DirectoryBusterModule:
    def __init__(self, target_url, session, method='GET', wordlist=None, threads=10, extensions=None):
        self.target_url = target_url.rstrip('/')
        self.session = session
        self.method = method
        self.threads = threads
        self.extensions = extensions or ['', '.php', '.html', '.txt', '.bak', '.old', '.backup', '.zip', '.tar', '.gz', '.log', '.tmp', '.swp']

        # Wordlist por defecto
        self.wordlist = self.load_wordlist_from_file(wordlist) or [
            'admin', 'login', 'wp-admin', 'administrator', 'phpmyadmin',
            'backup', 'uploads', 'images', 'css', 'js', 'api', 'test',
            'config', 'include', 'tmp', 'cgi-bin', 'secret', 'hidden',
            'assets', 'static', 'public', 'private', 'vendor', 'lib',
            'src', 'app', 'system', 'core', 'modules', 'plugins',
            'themes', 'database', 'logs', 'cache', 'temp', 'downloads',
            'files', 'content', 'media', 'resources',
            'node_modules', 'bower_components', 'dist', 'build', 'inc',
            'includes', 'classes', 'wp-content', 'wp-includes',
            'components', 'templates', 'sessions', '.git', '.svn',
            '.hg', '.env', '.aws', '.ssh', 'dev', 'test',
            'testing', 'stage', 'staging', 'qa', 'backups',
            'archive', 'conf', 'settings', 'error', 'errors',
            'v1', 'v2', 'v3', 'rest', 'graphql', 'swagger',
            'docs', 'apidoc', 'auth', 'authenticate', 'signin',
            'signup', 'register', 'forgot', 'reset', 'recover',
            'logout', 'session', 'sessions', 'user', 'users', 'profile'
        ]

        self.module_name = "[+] Directory Buster"
        self.results = {}

        print(self.module_name)
        self.execute()

    def load_wordlist_from_file(self, filepath):
        # Carga una wordlist desde archivo si es indicada
        try:
            with open(filepath, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
            return wordlist
        except FileNotFoundError:
            print(f"[!] Archivo de wordlist no encontrado: {filepath}")
            return None
        except Exception as e:
            print(f"[!] Error cargando wordlist: {e}")
            return None
    

    def execute(self):
        # Ejecuta el escaneo de directorios
        print(f"\n[+] Iniciando Directoyu Buster en: {self.target_url}")
        print(f"\n[+] Threads: {self.threads}")
        print(f"\n[+] Wordlist: {len(self.wordlist)} entradas")
        print(f"\n[+] Escaneando")

        # URL a probar

        urls_to_check = []

        for directory in self.wordlist:
            urls_to_check.append(f"{self.target_url}/{directory}/")


        # Añadir archivos
        for directory in self.wordlist:
            for ext in self.extensions:
                if ext:
                    urls_to_check.append(f"{self.target_url}/{directory}{ext}")
        
        total_urls = len(urls_to_check)
        print(f"[+] Total de URLs a probar: {total_urls}\n")

        found_dirs = []
        found_files = []
        checked = 0

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_url, url): url for url in urls_to_check}

            for future in as_completed(futures):
                checked += 1
                result = future.result()

                if result:
                    if result['type'] == 'directory':
                        found_dirs.append(result)
                    else:  
                        found_files.append(result)

        self.results = {
            'directories': found_dirs,
            'files': found_files,
            'total_found': len(found_dirs) + len(found_files),
            'total_checked': total_urls,
            'target': self.target_url
        }

        self.report()
        return self.results
    
    def check_url(self, url):
        # Verifíca si una URL existe - filtro antispam

        try:
            response = self.session.request(
                method=self.method,
                url=url,
                timeout = 5,
                allow_redirects=False
            )

            if response.status_code in [200, 301, 302, 403, 405]:

                # Verificar página error genérica
                content = response.text.lower()
                error_patterns = [
                    '404 not found', 'page not found', 'the requested url was not found',
                    '404 error', 'file not found', 'does not exist',
                    'the page you requested was not found', 'sorry, the page you are looking for could not be found'
                ]

                # 200 pero contenido 404
                if response.status_code == 200:
                    for pattern in error_patterns:
                        if pattern in content:
                            return None
                        
                # Determinar tipo
                is_directory = url.endswith('/')

                return {
                    'url': url,
                    'status_code': response.status_code,
                    'content_length': len(response.content),
                    'type': 'directory' if is_directory else 'file',
                    'is_redirect' : response.is_redirect,
                    'location': response.headers.get('Location') if response.is_redirect else None
                }

  
        except Exception:
            return None

    def report(self):
        """Muestra los resultados encontrados"""
        directories = self.results.get('directories', [])
        files = self.results.get('files', [])
        total = self.results.get('total_found', 0)
        total_checked = self.results.get('total_checked', 0)
        
        print(f"\n{'='*60}")
        print(f"[*] DIRECTORY BUSTER REPORT")
        print(f"{'='*60}")
        
        if total == 0:
            print("\n[!] No se encontraron directorios o archivos")
            print(f"[+] Total URLs probadas: {total_checked}")
            print(f"{'='*60}")
            return
        
        # Mostrar directorios
        if directories:
            print(f"\n[+] DIRECTORIOS ENCONTRADOS: {len(directories)}")
            for d in directories:
                status_color = '\033[92m' if d['status_code'] == 200 else '\033[93m'
                print(f"  {status_color}{d['url']} - {d['status_code']}\033[0m")
                if d.get('location'):
                    print(f"    → Redirige a: {d['location']}")
        
        # Mostrar archivos
        if files:
            print(f"\n[+] ARCHIVOS ENCONTRADOS: {len(files)}")
            for f in files:
                status_color = '\033[92m' if f['status_code'] == 200 else '\033[93m'
                print(f"  {status_color}{f['url']} - {f['status_code']}\033[0m")
                if f.get('location'):
                    print(f"    → Redirige a: {f['location']}")
        
        print(f"\n[+] Total encontrado: {total}")
        print(f"[+] Total URLs probadas: {total_checked}")
        print(f"{'='*60}")
    
    def export_results(self, filename=None):
        """Exporta los resultados a un archivo"""
        if not filename:
            filename = f"directory_buster_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Directory Buster Report\n")
                f.write(f"{'='*50}\n")
                f.write(f"Target: {self.target_url}\n")
                f.write(f"Total URLs probadas: {self.results['total_checked']}\n")
                f.write(f"Total encontrados: {self.results['total_found']}\n")
                f.write(f"{'='*50}\n\n")
                
                if self.results['directories']:
                    f.write(f"DIRECTORIOS ENCONTRADOS:\n")
                    for d in self.results['directories']:
                        f.write(f"  {d['url']} - {d['status_code']}\n")
                
                if self.results['files']:
                    f.write(f"\nARCHIVOS ENCONTRADOS:\n")
                    for f_item in self.results['files']:
                        f.write(f"  {f_item['url']} - {f_item['status_code']}\n")
            
            print(f"\n[+] Resultados exportados a: {filename}")
            
        except Exception as e:
            print(f"\n[!] Error exportando: {e}")