import os
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Blacklist():
    def __init__(self):
        self.filename = 'blacklist.txt'
        self.create_file()

    def create_file(self):
        if os.path.isfile(self.filename) is False:
            open(self.filename, 'w').close()

    def reset(self):
        open(self.filename, 'w').close()

    @property
    def domains(self):
        with open(self.filename) as f:
            domains = [i.strip() for i in f.readlines()]
        return domains

    def add(self, URL):
        domain = urlparse(URL).netloc.replace('www.', '').strip()
        if domain not in self.domains:
            with open(self.filename, 'a') as f:
                f.write(domain + '\n')
        return domain

    def delete(self, domain):
        domains = self.domains
        self.reset()
        for i in domains:
            if i == domain:
                pass
            else:
                with open(self.filename, 'a') as f:
                    f.write(i + '\n')

    def query_string(self):
        query_string = ''
        exclude = '-site:'
        for domain in self.domains:
            exclude_domain = exclude + domain + ' '
            query_string = query_string + exclude_domain
        return query_string.strip()
