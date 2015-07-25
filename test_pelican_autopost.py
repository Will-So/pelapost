import pytest
from pelican_auto_post import make_md, publish, copy_notebook, BLOG_DIR
import os

TEST_DIR = '/Users/Will/Devel/pelican_autopost/testdir/'
NOTEBOOK_DIR = TEST_DIR + 'content/notebooks/'

SKIP_PUBLISH = True

@pytest.mark.xfail(raises=IOError)
def test_markdown_safe():
    """
    Tests that we cannot write to a directory twice
    """
    make_md(TEST_DIR, "test", "blah", 'blah')
    make_md(TEST_DIR, "test", "blah", 'blah')


def test_notebook_copy():
    copy_notebook(NOTEBOOK_DIR + 'sqlite3_CLI.ipynb', TEST_DIR, 'test')
    assert os.path.exists(NOTEBOOK_DIR + 'test.ipynb')


def test_make_md():
    """
    Verifies that 1) an md file is created with the correct format and
     2) that all the options are  correctly set
    """
    if os.path.exists(TEST_DIR + 'content/test.md'):
        os.remove(TEST_DIR + 'content/test.md')
    make_md(TEST_DIR, "test", "blah", 'blah')
    assert os.path.exists(TEST_DIR + 'content/test.md')


@pytest.mark.skipif(SKIP_PUBLISH, reason='skip')
def test_publish():
    """
    Tests whether the file is uploaded properly to github.

    We use our default blog_dir in this case because otherwise
    we need to set up an entire new blog.

    test is disabled by default.
    """
    publish(BLOG_DIR)


@pytest.fixture
def del_files(request):
    """
    Deletes markdown file after test is run
    """
    def fin():
        if os.path.exists(TEST_DIR + 'test.md'):
            os.remove(TEST_DIR + 'test.md')
    request.addfinalizer(fin)
    return del_files