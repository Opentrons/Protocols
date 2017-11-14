import os
import tempfile
import zipfile

from protolib import utils


def test_zip_file():
    data = 'foo bar...'
    ifile_name = 'ifile.json'
    ifile = os.path.join(tempfile.gettempdir(), ifile_name)
    ofile = os.path.join(tempfile.gettempdir(), 'ofile.json')

    with open(ifile, 'w') as f:
        f.write(data)

    utils.zip_file([ifile], ofile)

    with zipfile.ZipFile(ofile) as zf:
        with zf.open(ifile_name) as f:
            assert f.read().decode() == data


def test_tag_from_ci_env_vars():
    ci_name = 'Travis-CI'
    pull_request_var = 'TRAVIS_PULL_REQUEST'
    branch_var = 'TRAVIS_BRANCH'
    commit_var = 'TRAVIS_COMMIT'

    os.environ[pull_request_var] = '1-fake-PR'
    os.environ[branch_var] = '211-fake-branch'
    os.environ[commit_var] = '12345'

    tag = utils.tag_from_ci_env_vars(
        ci_name, 'false', branch_var, commit_var
    )
    assert tag == '211-fake-branch_12345'

    tag = utils.tag_from_ci_env_vars(
        ci_name, pull_request_var, branch_var, commit_var
    )
    assert tag == 'pull_1'
