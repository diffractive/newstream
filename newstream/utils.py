import json

from django.conf import settings

from i18nfield.strings import LazyI18nString

# i18n strings
# We use this so we can set default values based on i18n strings, and dynamically
# set the default at runtime when the models are created / migrated
def resolve_i18n_string(i18n_str):
    value = LazyI18nString.from_gettext(_(i18n_str)).data
    return json.dumps({lng: value[lng] for lng, lngname in settings.LANGUAGES if value[lng]}, sort_keys=True)



