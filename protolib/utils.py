#!/usr/bin/env python

import datetime as dt
import os
import re
import zipfile


script_tag = "[OT-PL-Lib build] "
script_tab = "                  "


def tag_from_ci_env_vars(ci_name, pull_request_var, branch_var, commit_var):
    pull_request = os.environ.get(pull_request_var)
    branch = os.environ.get(branch_var)
    commit = os.environ.get(commit_var)

    if pull_request and pull_request != 'false':
        try:
            pr_number = int(re.findall("\d+", pull_request)[0])
            print(script_tab + "Pull Request valid {} variable found: "
                               "{}".format(ci_name, pr_number))
            return 'pull_{}'.format(pr_number)
        except (ValueError, TypeError):
            print(
                script_tab + 'The pull request environmental variable {} '
                             'value {} from {} is not a valid number'
                .format(pull_request_var, pull_request, ci_name)
            )

    if branch and commit:
        print(
            script_tab + "\tBranch and commit valid {} variables found "
                         "{} {}"
            .format(ci_name, branch, commit)
        )
        return "{}_{}".format(branch, commit[:10])
    return ""


def get_build_name():
    print(script_tag + "Checking Travis-CI environment variables for tag:")
    ci_tag = tag_from_ci_env_vars(
        ci_name='Travis-CI',
        pull_request_var='TRAVIS_PULL_REQUEST',
        branch_var='TRAVIS_BRANCH',
        commit_var='TRAVIS_COMMIT'
    )
    time_stamp = dt.datetime.now().strftime("%Y-%m-%d_%H.%M")

    tag = time_stamp
    if ci_tag:
        tag = "{}_{}".format(tag, ci_tag)
    return tag


def zip_file(ifiles, ofile):
    zip_output = zipfile.ZipFile(ofile, 'w', zipfile.ZIP_DEFLATED)
    for ifile in ifiles:
        zip_output.write(ifile, os.path.basename(ifile))
