# import sentry for error logging
# import sentry_sdk
# sentry_sdk.init("https://fd5b6fe456a64e8f91d7c424f3a35003@sentry.io/1442181")

import lazy_import

lazy_import.lazy_module("redtoolkit.scidata")
lazy_import.lazy_module("redtoolkit.textanalysis")
lazy_import.lazy_module("redtoolkit.utils")
lazy_import.lazy_module("redtoolkit.visualizers")
lazy_import.lazy_module("redtoolkit.wrappers")


# import top level modules
# from redtoolkit import scidata
# from redtoolkit import textanalysis
# from redtoolkit import utils
# from redtoolkit import visualizers
# from redtoolkit import wrappers

# version
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
