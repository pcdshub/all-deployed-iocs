import json


def list_hosts() -> set[str]:
    """List all IOC hosts in use. """

    with open("iocs.json", "rb") as fp:
        raw_iocs = json.load(fp)

    return {ioc["host"] for ioc in raw_iocs}


if __name__ == "__main__":
    hosts = list_hosts()
    for host in sorted(hosts):
        print(host)
