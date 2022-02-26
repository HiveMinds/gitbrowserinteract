import argparse

from .helper import get_browser_drivers
from .Hardcoded import Hardcoded
from .Main import Main
from .Ssh_deploy_key_setter import Ssh_deploy_key_setter
from .Github_personal_access_token_getter import Github_personal_access_token_getter

print(
    f"\n\nHi, I'll ask you from which source repo to which target repo you want to copy the issues, then I'll download browser controllers and ensure the firefox browser is installed. Next I will scrape the issues from the source repo, and add them as new issues to the target repo. You can simply see what I do in the browser. Terminate me with CTRL+C if you don't like it. I'll let you know when I'm done."
)
project_nr = 1

# get browser drivers
hc = Hardcoded()
get_browser_drivers(hc)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--g",
    dest="gitlab_runner",
    action="store_true",
    help="boolean flag, determines whether the code gets the GitLab Runner token or not.",
)
parser.add_argument(
    "--d",
    dest="deploy_token",
    action="store_true",
    help="boolean flag, determines whether the code gets the deploy token or not",
)
parser.add_argument(
    "--ssh",
    dest="public_ssh_sha",
    # action="store_true", # This is not a boolean, but stores the incoming argument value (ssh key)
    type=str,
    help="Indicator letting Python know the public ssh key is being passed to python. This key is then stored in the python variable:public_ssh_sha",
)
parser.add_argument(
    "--hubcpat",
    dest="github_commit_status_personal_access_token_flag",
    action="store_true",
    help="boolean flag, determines whether the code gets the personal access token to set the build statusses of commits in GitHub.",
)

parser.add_argument(
    "-hu",
    dest="github_username",
    type=str,
    help="Indicator letting Python know the GitHub username is being passed next.",
)

parser.add_argument(
    "-hp",
    dest="github_pwd",
    type=str,
    help="Indicator letting Python know the GitHub password is being passed next.",
)

parser.set_defaults(
    gitlab_runner=True,
    deploy_token=False,
    github_commit_status_personal_access_token_flag=False,
    github_username=None,
    github_pwd=None,
)
args = parser.parse_args()
if args.deploy_token:
    print(f"Setting and getting GitHub ssh-deploy key (NOT TOKEN).")
    args.gitlab_runner = False
    print(f"The ssh deploy key is:={args.public_ssh_sha}")
    ssh_deploy_key_setter = Ssh_deploy_key_setter(
        project_nr=project_nr,
        public_ssh_sha=args.public_ssh_sha,
        github_username=args.github_username,
        github_pwd=args.github_pwd,
    )
elif args.github_commit_status_personal_access_token_flag:
    print(
        f"Getting GitHub personal access token to be able to set GitHub commit build statuses."
    )
    args.gitlab_runner = False
    args.deployment_token = False
    github_personal_access_token_getter = Github_personal_access_token_getter(
        project_nr=project_nr,
        github_username=args.github_username,
        github_pwd=args.github_pwd,
    )
elif args.gitlab_runner:
    print(f"Getting GitLab runner token.")
    args.gitlab_runner = False
    main = Main(project_nr)


print(f"Done.")
