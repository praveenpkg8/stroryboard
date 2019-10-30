import os
import sys
import unittest


def fixup_paths(path):

    try:
        import google
        google.__path__.append("{0}/google".format(path))
    except ImportError:
        print("import error")

    sys.path.insert(1, path)


def main(sdk_path, test_path, test_pattern):

    if os.path.exists(os.path.join(sdk_path, 'platform/google_appengine')):
        sdk_path = os.path.join(sdk_path, 'platform/google_appengine')

    fixup_paths(sdk_path)

    import dev_appserver
    dev_appserver.fix_sys_path()

    try:
        import appengine_config
        (appengine_config)

    except ImportError:
        print('Issue in Importing appengine_config module')


    print 'Discovering tests in : {}'.format(test_path)
    suite = unittest.TestLoader().discover(test_path, test_pattern)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result


if __name__ == '__main__':
    sdk_path = os.environ['gcloud_path']
    sdk_path = sdk_path or '/Users/user/google-cloud-sdk'
    test_path = os.path.dirname(os.path.abspath(__name__)) + '/test'
    test_pattern = 'test_*'

    result = main(sdk_path, test_path, test_pattern)

    if not result.wasSuccessful():
        sys.exit(1)

