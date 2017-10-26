import os


def getTravisBranch():
    # https://graysonkoonce.com/getting-the-current-branch-name-during-a-pull-request-in-travis-ci/  # noqa: E501
    if os.environ.get('TRAVIS_PULL_REQUEST') == 'false':
        return os.environ.get('TRAVIS_BRANCH')
    else:
        # don't use TRAVIS_BRANCH -- that is the PR target (eg, master)
        return os.environ.get('TRAVIS_PULL_REQUEST_BRANCH')


def getProtolibBranch():
    # Map Protocols repo branch name to protocol-library protolib branch.
    branchmapping = {
        'master': 'master',
        'develop': 'develop',
        'experimental': 'experimental',  # create this
        'remove-times': 'remove-times'  # remove this
        # Add more here
    }

    travis_branch = getTravisBranch()
    fallback = 'master'
    return branchmapping.get(travis_branch, fallback)


if __name__ == '__main__':
    import sys

    err = 'Invalid arg. Run this script like \
        "python getBranch.py [protolib|upload]"'

    if len(sys.argv) != 2:
        raise ValueError(err)
    if sys.argv[1] == 'protolib':
        print(getProtolibBranch())
    elif sys.argv[1] == 'upload':
        # Upload using the branch name, no mapping!
        print(getTravisBranch())
    else:
        raise ValueError(err)
