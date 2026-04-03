import requests


class APIExtractionMachine:
    def __init__(self, login_url, credentials):
        self.session = requests.Session()
        self.login_url = login_url
        self.credentials = credentials
        self.token = None

    def _execute_login(self):
        try:
            response = self.session.post(
                self.login_url,
                json=self.credentials,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            token = data.get("token")
            if token is None:
                return False
            self.token = token
            self.session.headers.update(
                {"Authorization": f"Bearer {self.token}"}
            )
            return True
        except requests.exceptions.RequestException:
            return False

    def fetch_data_with_retry(self, data_url):
        try:
            response = self.session.get(data_url, timeout=30)
        except requests.exceptions.RequestException:
            return None

        if response.status_code == 200:
            return response.json()

        if response.status_code in (401, 403):
            if not self._execute_login():
                return None
            try:
                response = self.session.get(data_url, timeout=30)
            except requests.exceptions.RequestException:
                return None
            if response.status_code == 200:
                return response.json()
            return None

        return None
