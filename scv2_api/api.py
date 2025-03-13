import requests

class SalesCloudV2Session:

    __hostname : str = ''

    __use_secure_http : bool = True

    __username : str = ''

    __password : str = ''

    __default_timeout : int

    __session : requests.Session

    def __init__(self, hostname : str, username : str, password : str):
        
        self.__hostname = hostname

        self.__username = username

        self.__password = password

        self.set_default_timeout(180)
        self.set_ssl_verify(True)

    def connect(self):

        self.__session = requests.Session()

        self.__session.auth = (self.__username, self.__password)

    def set_default_timeout(self, timeout : int):
        self.__default_timeout = timeout

    def set_ssl_verify(self, ssl_verify : bool):
        self.__session.verify = ssl_verify

    def get(self) -> requests.Response:
        pass

    def post(self) -> requests.Response:
        pass

    def patch(self) -> requests.Response:
        pass

    def put(self) -> requests.Response:
        pass

    def delete(self) -> requests.Response:
        pass