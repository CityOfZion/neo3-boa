import logging
import os
import platform
import stat
import sys

import requests

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_umask():
    umask = os.umask(0)
    os.umask(umask)
    return umask


def chmod_plus_x(path):
    os.chmod(
        path,
        os.stat(path).st_mode |
        (
            (
                stat.S_IXUSR |
                stat.S_IXGRP |
                stat.S_IXOTH
            )
            & ~get_umask()
        )
    )


def main():
    if not sys.maxsize > 2 ** 32:
        print("CPM is not supported on 32-bit platforms")

    r = requests.get("https://api.github.com/repos/CityOfZion/cpm/releases")

    for release in r.json():
        tag = release['tag_name']
        version = tag[1:]
        if platform.machine().lower() in ["x86_64", "amd64"]:
            arch = "amd64"
        else:
            arch = "arm64"
        system = platform.system().lower()
        asset_needle = f"cpm_{version}_{system}_{arch}"
        if system == "windows":
            asset_needle += ".exe"

        for asset in release['assets']:
            if asset['name'] == asset_needle:
                r = requests.get(asset['browser_download_url'], stream=True)
                print(f"Found release! Downloading {asset['browser_download_url']}...", end='')

                cpm_filename = f"{os.path.dirname(sys.argv[0])}/cpm"
                if system == "windows":
                    cpm_filename += ".exe"

                with open(cpm_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                if system in ["darwin", "linux"]:
                    chmod_plus_x(cpm_filename)
                print("done")
                return


if __name__ == "__main__":
    main()
