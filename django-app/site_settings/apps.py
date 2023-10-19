import requests
import urllib3
from google.oauth2 import service_account
from google.cloud.storage import Blob, Client
from google.api_core.client_options import ClientOptions
from django.core.files.storage import default_storage
from django.conf import settings
from django.apps import AppConfig

class SiteSettingsConfig(AppConfig):
    name = 'site_settings'

    def ready(self):
        # put your startup code here
        # Override gcloud config (monkey patch)
    
        # disable SSL validation
        # disable https warnings for https insecure certs
        my_http = requests.Session()
        my_http.verify = False
        urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
        )

        storage = default_storage
        if settings.GS_STORAGE_ENDPOINT:
            storage._client = Client(
                project=storage.project_id,
                credentials=storage.credentials,
                _http=my_http,
                client_options = ClientOptions(api_endpoint=settings.GS_STORAGE_ENDPOINT)
            )

        print("GCS Configured")
