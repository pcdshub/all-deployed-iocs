import io
import json
import sys
from typing import Generator

import git


def is_same(d1: dict[str, str], d2: dict[str, str]) -> bool:
    """
    Are d1/d2 the 'same' as far as deployed IOCs are concerned?

    Parameters
    ----------
    d1 : dict[str, str]

    d2 : dict[str, str]


    Returns
    -------
    bool

    """
    if set(d1) != set(d2):
        return False
    return all(d1[k] == d2[k] for k in d1)


def get_changes(
    d1: dict[str, str], d2: dict[str, str]
) -> Generator[tuple[str, str], None, None]:
    """
    Get changes between d1 -> d2.

    Parameters
    ----------
    d1 : dict[str, str]

    d2 : dict[str, str]


    Returns
    -------
    Generator[tuple[str, str], None, None]

    """
    for key in set(d2) - set(d1):
        yield key, f"{d2[key]}"

    for key in set(d1) - set(d2):
        yield key, f"(deleted key)"

    for key in d2:
        if key in d1 and d1[key] != d2[key]:
            yield key, f"{d2[key]}"


def print_changes(ioc: str) -> None:
    """
    Print the changes made to IOC manager for the given IOC.

    Parameters
    ----------
    ioc : str
        The IOC name.
    """
    last = {}
    for commit in git.Repo(".").iter_commits(reverse=True):
        try:
            blob = commit.tree / "iocs.json"
        except KeyError:
            continue

        with io.BytesIO() as fp:
            blob.stream_data(fp)
            raw_iocs = json.loads(fp.getvalue().decode("utf-8"))

        iocs = {ioc["name"]: ioc for ioc in raw_iocs}

        changed = list(get_changes(last, iocs[ioc]))
        if changed:
            print()
            print(f"{commit.committed_datetime}")  #  {commit.author.name}")

            for key, change in changed:
                print(f"  {key}: {change}")

            last = iocs[ioc]


if __name__ == "__main__":
    ioc = sys.argv[1]
    print_changes(ioc)
