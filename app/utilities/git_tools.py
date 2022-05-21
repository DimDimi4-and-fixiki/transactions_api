import git
from typing import AnyStr, Any


def get_git_signature(path: AnyStr = None):

    # Get sha git signature from current project directory
    if path is None:
        try:
            repo = git.Repo(search_parent_directories=True)
            sha = repo.head.object.hexsha
            return sha
        except git.exc.InvalidGitRepositoryError:
            return 'no Git repository found'

