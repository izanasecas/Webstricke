import requests
import time
class BasicRequestModule:
    def __init__(self, target_url, session, method="GET"):
        self.target_url = target_url
        self.session = session
        self.method = method
        self.module_name = "[+] Basic Infortamtion"
        print(self.module_name)

        self.execute()

    def execute(self):
        try:
            t1 = time.time()
            req = self.session.request(method=self.method, url=self.target_url, timeout=3, allow_redirects=False)
            t2 = time.time()

            results = {
                'status_code': req.status_code,
                'response_time': round(t2-t1, 3),
                'response_headers': dict(req.headers),
                'final_url': req.url,
                'is_redirect': req.is_redirect,
                'redirect_location': req.headers.get('Location') if req.is_redirect else None
            }
            print(results)
            self.results = results
            self.report()

            return results
        
        except Exception as e:
            print(f"\n\n[!] Ha habido un error: %s" % e)


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
        print(f"    [*] Server info:")
        print(f"\t Server: {server}")
        print(f"\t Tecnologías: {self.technologies(server)}")
        print(f"\t Content-Type: {content_type}")
        if self.results.get('is_redirect'):
            location = self.results.get('redirect_location', 'No especificada')
            print(f"\n    [*] REDIRECCIÓN DETECTADA:")
            print(f"\t Código: {self.results['status_code']}")
            print(f"\t Destino: {location}")
            quest = input("\t Quieres seguir la redirección? (Si/No): ")

            if 'Si' in quest:
                BasicRequestModule(location, self.session)
        else:
          print(f"\n    [*] Sin redirecciones")

       
