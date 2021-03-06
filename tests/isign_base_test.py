from os.path import dirname, exists, join, isdir
from isign import isign
import logging
from monitor_temp_file import MonitorTempFile
import os
import shutil
import tempfile
import unittest

log = logging.getLogger(__name__)


class IsignBaseTest(unittest.TestCase):
    TEST_DIR = dirname(__file__)
    TEST_APPS_MISC_DIR = join(TEST_DIR, 'apps', 'misc')
    TEST_XCODE7_DIR = join(TEST_DIR, 'apps', 'xcode7')
    TEST_XCODE11_DIR = join(TEST_DIR, 'apps', 'xcode11')

    # Things that aren't apps; these should raise exceptions
    TEST_NONAPP_DIR = join(TEST_APPS_MISC_DIR, 'NotAnAppDir')
    TEST_NONAPP_TXT = join(TEST_APPS_MISC_DIR, 'NotAnApp.txt')
    TEST_NONAPP_IPA = join(TEST_APPS_MISC_DIR, 'NotAnApp.ipa')

    # XCode7 ipas, and apps in other formats:
    TEST_APP_XCODE7 = join(TEST_XCODE7_DIR, 'Test.app')  # FIXME, ios11+ or maybe don't even bother any more
    TEST_APP_CODESIG_STR_XCODE7 = join(
        TEST_XCODE7_DIR,
        'Test.app.codesig.construct.txt'
    )  # FIXME, ios11+
    TEST_APPZIP_XCODE7 = TEST_APP_XCODE7 + '.zip'  # FIXME, ios11+ or maybe don't even bother any more
    TEST_IPA_XCODE7 = join(TEST_XCODE7_DIR, 'Test.ipa')
    TEST_WITH_FRAMEWORKS_IPA_XCODE7 = join(TEST_XCODE7_DIR, 'TestWithFrameworks.ipa')  # FIXME, ios11+
    TEST_SIMULATOR_APP_XCODE7 = join(TEST_XCODE7_DIR, 'TestSimulator.app.zip')  # FIXME, ios11+

    # These were added in a PR; variants of Test.app
    TEST_UNSIGNED_THIN_APP = join(TEST_XCODE7_DIR, 'Test_unsigned_thin.app')
    TEST_UNSIGNED_FAT_APP = join(TEST_XCODE7_DIR, 'Test_unsigned_fat.app')

    # XCode11 ipas
    # See the isignpy Github org for sources
    TEST_IPA_XCODE11 = join(TEST_XCODE11_DIR, 'isignTestApp.ipa')  # A simple test app
    TEST_FRAMEWORKS_IPA_XCODE11 = join(TEST_XCODE11_DIR, 'isignFrameworksTestApp.ipa')  # ...with a cocoapods framework
    TEST_WATCH_IPA_XCODE11 = join(TEST_XCODE11_DIR, 'isignTestWatchApp.ipa')  # ...with WatchOS app and related appex

    # Credentials
    KEY = join(TEST_DIR, 'credentials', 'test.key.pem')
    CERTIFICATE = join(TEST_DIR, 'credentials', 'test.cert.pem')
    PROVISIONING_PROFILE = join(TEST_DIR, 'credentials', 'test.mobileprovision')
    CREDENTIALS_DIR = join(TEST_DIR, 'credentials_std_names')
    CREDENTIALS_DIR_2 = join(TEST_DIR, 'credentials_std_names_2')

    ERROR_KEY = '_errors'

    # Fake Apple organizational unit
    OU = 'ISIGNTESTS'

    def setUp(self):
        """ this helps us monitor if we're not cleaning up temp files """
        MonitorTempFile.start()

    def tearDown(self):
        """ remove monitor on tempfile creation """
        remaining_temp_files = MonitorTempFile.get_temp_files()
        MonitorTempFile.stop()
        if len(remaining_temp_files) != 0:
            log.error("remaining temp files: %s",
                      ', '.join(remaining_temp_files))

    #        assert len(remaining_temp_files) == 0

    def resign(self, filename, **args):
        """ resign with test credentials """
        args.update({
            "key": self.KEY,
            "certificate": self.CERTIFICATE,
            "provisioning_profiles": [self.PROVISIONING_PROFILE]
        })
        return isign.resign(filename, **args)

    def resign_adhoc(self, filename, **args):
        return isign.resign_adhoc(filename, **args)

    def unlink(self, path):
        if exists(path):
            if isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)

    def get_temp_file(self, prefix='isign-test-'):
        """ just getting a file path that probably isn't in use """
        (fd, path) = tempfile.mkstemp(prefix=prefix)
        os.close(fd)
        os.unlink(path)
        return path

    def get_temp_dir(self, prefix='isign-test-'):
        return tempfile.mkdtemp(prefix=prefix)
