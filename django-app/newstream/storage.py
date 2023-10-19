from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import clean_name
from google.cloud.storage.blob import _quote

from django.utils.deconstruct import deconstructible

@deconstructible
class NewstreamCloudStorage(GoogleCloudStorage):

    def url(self, name):
        """
        We override this to never use a signed URL. We are serving media files
        directly via our backend
        """
        name = self._normalize_name(clean_name(name))

        return '{storage_base_url}/{quoted_name}'.format(
            storage_base_url=self.custom_endpoint,
            quoted_name=_quote(name, safe=b"/~"),
        )