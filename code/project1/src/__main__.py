import argparse

from .Main import Main
from .Deployment_token_getter import Deployment_token_getter

print(
    f"Hi, I'll ask you from which source repo to which target repo you want to copy the issues, then I'll download browser controllers and ensure the firefox browser is installed. Next I will scrape the issues from the source repo, and add them as new issues to the target repo. You can simply see what I do in the browser. Terminate me with CTRL+C if you don't like it. I'll let you know when I'm done."
)
project_nr = 1

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
parser.set_defaults(
    gitlab_runner=True,
    deploy_token=False,
)
args = parser.parse_args()
if args.deploy_token:
    print(f"Getting GitHub deploy token.")
    args.gitlab_runner=False
    deployment_token_getter = Deployment_token_getter(project_nr)
elif args.gitlab_runner:
    print(f"Getting GitLab runner token.")
    args.gitlab_runner=False
    main = Main(project_nr)



print(f"Done.")
