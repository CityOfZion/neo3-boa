import sys

import requests
import platform
import os
import stat

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
    r = requests.get("https://api.github.com/repos/CityOfZion/cpm/releases")

    for release in r.json():
        tag = release['tag_name']
        version = tag[1:]
        if "x86_64" == platform.machine().lower():
            arch = "amd64"
        else:
            # TODO: need somebody with ARM cpu to tell me what "machine()" prints because now 32-bit intel will also be labelled as arm
            arch = "arm64"
        system = platform.system().lower()
        asset_needle = f"cpm_{version}_{system}_{arch}"
        for asset in release['assets']:
            if asset['name'] == asset_needle:
                r = requests.get(asset['browser_download_url'], stream=True)
                cpm_filename = f"{os.path.dirname(sys.argv[0])}/cpm"
                with open(cpm_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                if system in ["darwin", "linux"]:
                    chmod_plus_x(cpm_filename)
                else:
                    # TODO: check permissions windows
                    print("yikes, this is windows. Is it executable?")


if __name__ == "__main__":
    main()
