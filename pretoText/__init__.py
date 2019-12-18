# import sentry for error logging
# import sentry_sdk
# sentry_sdk.init("https://fd5b6fe456a64e8f91d7c424f3a35003@sentry.io/1442181")

import lazy_import

lazy_import.lazy_module("pretoText.Patent")

# version
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
