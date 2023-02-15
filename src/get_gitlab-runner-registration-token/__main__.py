"""Entry point for the project."""

from typing import List

from meme.create_gif import create_gif
from meme.create_meme_content import create_meme_content

# Parse user arguments to determine what to do.
parser = argparse.ArgumentParser()
parser.add_argument(
    "--glr",
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
    help=(
        "Indicator letting Python know the public ssh key is being passed to "
        + "python. This key is then stored in the python variable:public_ssh_sha"
    ),
)
parser.add_argument(
    "--hubcpat",
    dest="github_commit_status_personal_access_token_flag",
    action="store_true",
    help=(
        "boolean flag, determines whether the code gets the personal access "
        + "token to set the build statusses of commits in GitHub."
    ),
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
    gitlab_runner=False,
    deploy_token=False,
    github_commit_status_personal_access_token_flag=False,
    github_username=None,
    github_pwd=None,
)
args = parser.parse_args()
if args.deploy_token:
    print("Setting and getting GitHub ssh-deploy key (NOT TOKEN).")
    args.gitlab_runner = False
    print(f"The ssh deploy key is:={args.public_ssh_sha}")
    _ = Ssh_deploy_key_setter(
        project_nr=project_nr,
        public_ssh_sha=args.public_ssh_sha,
        github_username=args.github_username,
        github_pwd=args.github_pwd,
    )
elif args.github_commit_status_personal_access_token_flag:
    print(
        "Getting GitHub personal access token to be able to set"
        " GitHub commit build statuses."
    )
    args.gitlab_runner = False
    args.deployment_token = False
    _ = Github_personal_access_token_getter(
        project_nr=project_nr,
        github_username=args.github_username,
        github_pwd=args.github_pwd,
    )
elif args.gitlab_runner:
    print("Getting GitLab runner token.")
    # args.gitlab_runner = False
    _ = Get_gitlab_runner_token()


print("Done.")


Go_to_url