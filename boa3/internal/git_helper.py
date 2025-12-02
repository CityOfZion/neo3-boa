import subprocess


def _get_git_commit_hash(short: bool = True) -> str | None:
    try:
        arg = ['git', 'rev-parse', '--short', 'HEAD'] if short else ['git', 'rev-parse', 'HEAD']
        out = subprocess.check_output(arg, stderr=subprocess.DEVNULL, text=True).strip()
        return out or None
    except Exception:
        return None
