import requests
import time
class BasicRequestModule:
    def __init__(self, target_url, session, method="GET"):
        self.target_url = target_url
        self.session = session
        self.session.max_redirects = 5
        self.method = method
        self.module_name = "[+] Basic Infortamtion"
        print(self.module_name)

        self.execute()


    def execute(self):
        try:
            t1 = time.time()
            req = self.session.request(method=self.method, url=self.target_url, timeout=3, allow_redirects=True)
            t2 = time.time()

            results = {
                'status_code': req.status_code,
                'response_time': round(t2-t1, 3),
                'response_headers': dict(req.headers),
                'final_url': req.url,
                'redirect_count': len(req.history),
                'redirect_chain': req.history
            }
            
            print(results)
            security_analisys = self.analyze_security_headers(req.headers)
            results['security_headers'] = security_analisys

            self.results = results

            self.report()

            return results
        
        except Exception as e:
            print(f"\n\n[!] Ha habido un error: %s" % e)

    def analyze_security_headers(self, headers):
        security_headers = {
                'X-Frame-Options': {
                    'level': 'HIGH',
                    'good_values': ['DENY', 'SAMEORIGIN'],
                    'bad_values': ['ALLOW-FROM'],
                    'description': 'Protección contra clickjacking'
                },
                'X-XSS-Protection': {
                    'level': 'HIGH',
                    'good_values': ['1; mode=block', '1'],
                    'bad_values': ['0'],
                    'description': 'Protección XSS en navegadores antiguos'
                },
                'X-Content-Type-Options': {
                    'level': 'HIGH',
                    'good_values': ['nosniff'],
                    'bad_values': [],
                    'description': 'Previene MIME sniffing'
                },
                'Content-Security-Policy': {
                    'level': 'MEDIUM',
                    'good_values': [],  # Analizar más en profundidad
                    'bad_values': [],
                    'description': 'Política de seguridad de contenido'
                },
                'Strict-Transport-Security': {
                    'level': 'MEDIUM',
                    'good_values': [],  # Analizar que tenga max-age adecuado
                    'bad_values': [],
                    'description': 'Forza conexiones HTTPS (HSTS)'
                },
                'Referrer-Policy': {
                    'level': 'LOW',
                    'good_values': ['strict-origin-when-cross-origin', 'same-origin', 'strict-origin', 'no-referrer'],
                    'bad_values': ['unsafe-url', 'no-referrer-when-downgrade'],
                    'description': 'Controla información de referer'
                },
                'Permissions-Policy': {
                    'level': 'LOW',
                    'good_values': [],
                    'bad_values': [],
                    'description': 'Controla características del navegador'
                }
            }
        
        results = {}

        for header_name, header_info in security_headers.items():
             
            header_value = headers.get(header_name)

            result = {
                'present': header_value is not None,
                'value': header_value,
                'level': header_info['level'],
                'description': header_info['description'],
                'status': '[!] MISSING',
            }

            if header_value:
                # Header presente y evaluación
                if header_name == 'X-Frame-Options':
                    result['status'] = '[*] GOOD' if header_value in header_info['good_values'] else '[!] WEAK'
             
                elif header_name == 'X-XSS-Protection':
                    result['status'] = '[*] GOOD' if header_value in header_info['good_values'] else '[!] WEAK'
            
                elif header_name == 'X-Content-Type-Options':
                    result['status'] = '[*] GOOD' if header_value == 'nosniff' else '[!] WEAK'
             
                elif header_name == 'Referrer-Policy':
                    result['status'] = '[*] GOOD' if header_value in header_info['good_values'] else '[!] WEAK'
       
            else:
                # Header no presente
                result['status'] = '[!] MISSING'
            results[header_name] = result
                
        return results

    def technologies(self, technologi_msg):

        dict_technologies ={
        'Python': ['Python', 'Django', 'Flask', 'Werkzeug'],
        'PHP': ['PHP', 'Symfony', 'Laravel', 'CodeIgniter', 'Zend'],
        'ASP.NET': ['ASP.NET', 'IIS', '.NET', 'X-AspNet-Version', 'X-AspNetMvc-Version'],
        'Java': ['Java', 'JSP', 'Servlet', 'Spring', 'Tomcat', 'Jetty'],
        'Node.js': ['Node.js', 'Express', 'Node', 'npm'],
        'Ruby': ['Ruby', 'Rails', 'Ruby on Rails', 'Sinatra'],
        'Go': ['Go', 'Golang', 'Gin', 'Echo'],
        'Rust': ['Rust', 'Actix', 'Rocket'],
        'Nginx': ['nginx', 'Nginx'],
        'Apache': ['Apache', 'apache'],
        'IIS': ['IIS', 'Microsoft-IIS'],
        'Lighttpd': ['lighttpd', 'Lighttpd'],
        'Caddy': ['Caddy', 'caddy'],
        'Tomcat': ['Tomcat', 'Apache-Coyote'],
        'Jetty': ['Jetty', 'Eclipse-Jetty'],
        'Gunicorn': ['gunicorn', 'Gunicorn'],
        'uWSGI': ['uWSGI', 'uwsgi'],
        'Passenger': ['Passenger', 'Phusion Passenger'],
        'WordPress': ['wp-content', 'wp-includes', 'WordPress', 'wp-json'],
        'Drupal': ['Drupal', 'drupal-'],
        'Joomla': ['Joomla', 'joomla'],
        'Magento': ['Magento', 'magento'],
        'PrestaShop': ['PrestaShop', 'prestashop'],
        'Shopify': ['Shopify', 'shopify'],
        'WooCommerce': ['woocommerce', 'WooCommerce'],
        'Angular': ['angular', 'ng-', 'AngularJS'],
        'React': ['react', 'React', 'ReactJS'],
        'Vue.js': ['vue', 'Vue.js', 'vuejs'],
        'Bootstrap': ['bootstrap', 'Bootstrap'],
        'jQuery': ['jquery', 'jQuery'],
    }
        detected_technologies = []

        for tech, indicators in dict_technologies.items():
                for indicator in indicators:
                     if indicator.lower() in technologi_msg.lower():
                          detected_technologies.append(tech)
                          break

        if detected_technologies:
             return ', '.join(detected_technologies)
        else:   
            return("No reconocida")





    def report(self):
        server = self.results['response_headers'].get('Server', 'No especificado')
        content_type = self.results['response_headers'].get('Content-Type', 'No especificado')
        
        print(f"\n    [*] Status code: {self.results['status_code']}")
        print(f"    [*] Response time: {self.results['response_time']} seg")

        # Información del servidor
        print(f"    [*] Server info:")
        print(f"\t Server: {server}")
        print(f"\t Tecnologías: {self.technologies(server)}")
        print(f"\t Content-Type: {content_type}")

        # Información de redirecciones

        if self.results['redirect_count'] > 0:
               print(f"\n    [*] REDIRECCIONES SEGUIDAS: {self.results['redirect_count']}")
        for i, resp in enumerate(self.results['redirect_chain']):
            print(f"\t {i+1}. {resp.status_code} → {resp.headers.get('Location')}")
        print(f"\t Final: {self.results['status_code']} → {self.results['final_url']}")
            
        if self.results['redirect_count'] == 0:
            print(f"\n    [*] Sin redirecciones")

        # Información de headers de seguridad
        if 'security_headers' in self.results:
            print(f"\n    [*] SECURITY HEADERS:")
            security = self.results['security_headers']

            high_headers = [h for h, info in security.items() if info['level'] == 'HIGH']
            medium_headers = [h for h, info in security.items() if info['level'] == 'MEDIUM']
            low_headers = [h for h, info in security.items() if info['level'] == 'LOW']
            


            for header_name in high_headers + medium_headers + low_headers:
                info = security[header_name]
            
            # Color según estado
                if 'GOOD' in info['status']:
                    color = '\033[92m'  # Verde
                elif 'WEAK' in info['status']:
                    color = '\033[93m'  # Amarillo
                else:
                    color = '\033[91m'  # Rojo ← Para MISSING
                                
                print(f"\t {color}{info['status']}\033[0m {header_name}")
