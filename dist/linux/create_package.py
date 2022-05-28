import os
import shutil
import subprocess
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))


def clean():
    if os.path.exists(str(CURRENT_DIR) + "/dummyfilescreator.deb"):
        try:
            os.remove(str(CURRENT_DIR) + "/dummyfilescreator.deb")
        except OSError as error:
            print("error")

    if os.path.isdir(str(CURRENT_DIR) + "/dist"):
        try:
            shutil.rmtree(str(CURRENT_DIR) + "/dist")
        except (shutil.Error, OSError) as error:
            print("error")

    if os.path.isdir(str(CURRENT_DIR) + "/build"):
        try:
            shutil.rmtree(str(CURRENT_DIR) + "/build")
        except (shutil.Error, OSError) as error:
            print("error")

    if os.path.isdir(str(CURRENT_DIR) + "/package"):
        try:
            shutil.rmtree(str(CURRENT_DIR) + "/package")
        except (shutil.Error, OSError) as error:
            print("error")


def is_program_installed(program_name: str):
    return shutil.which(program_name)


def create_pyinstaller_dist():
    cmd = subprocess.call(
        ["pyinstaller", str(CURRENT_DIR) + "/linux.spec"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return cmd


def create_deb_package():
    cmd = subprocess.call(
        [
            "find",
            str(CURRENT_DIR) + "/package/opt/dummyfilescreator",
            "-type",
            "f",
            "-exec",
            "chmod",
            "644",
            "--",
            "{}",
            "+",
        ]
    )
    cmd = subprocess.call(
        [
            "find",
            str(CURRENT_DIR) + "/package/opt/dummyfilescreator",
            "-type",
            "d",
            "-exec",
            "chmod",
            "755",
            "--",
            "{}",
            "+",
        ]
    )
    cmd = subprocess.call(
        [
            "find",
            str(CURRENT_DIR) + "/package/usr/share",
            "-type",
            "f",
            "-exec",
            "chmod",
            "644",
            "--",
            "{}",
            "+",
        ]
    )
    cmd = subprocess.call(
        [
            "chmod",
            "+x",
            str(CURRENT_DIR) + "/package/opt/dummyfilescreator/dummy-files-creator",
        ]
    )
    cmd = subprocess.call(
        [
            "fpm",
            "-C",
            str(CURRENT_DIR) + "/package",
            "-s",
            "dir",
            "-t",
            "deb",
            "-n",
            "dummyfilescreator",
            "-v",
            "3.0.0",
            "-p",
            "dummyfilescreator.deb",
        ]
    )
    return cmd


def create_installer_folders():
    desktop_path = str(CURRENT_DIR) + "/package/usr/share/applications"
    icon_path = str(CURRENT_DIR) + "/package/usr/share/icons/hicolor/scalable/apps"

    try:
        os.makedirs(desktop_path)
        os.makedirs(icon_path)
    except OSError as error:
        print("error")


def copy_files():
    desktop_file = str(CURRENT_DIR) + "/var/dummy-files-creator.desktop"
    icon_file = str(CURRENT_DIR) + "/../../design/icon/icon.svg"
    dist_path = str(CURRENT_DIR) + "/dist"
    desktop_path = str(CURRENT_DIR) + "/package/usr/share/applications"
    icon_path = str(CURRENT_DIR) + "/package/usr/share/icons/hicolor/scalable/apps"
    opt_path = str(CURRENT_DIR) + "/package/opt"

    try:
        shutil.copy(desktop_file, desktop_path)
        shutil.copy(icon_file, icon_path)
        shutil.copytree(dist_path, opt_path)
    except (shutil.Error, OSError) as error:
        print("error")


def main():
    print("Checking if ruby is installed")
    if is_program_installed("ruby") == None:
        print("ruby is not installed")
        sys.exit(1)
    else:
        print("ruby is installed, proceeding...")

    print("Checking if fpm is installed")
    if is_program_installed("fpm") == None:
        print("fpm is not installed")
        sys.exit(1)
    else:
        print("fpm is installed, proceeding...")

    print("Checking if pyinstaller is installed")
    if is_program_installed("pyinstaller") == None:
        print("pyinstaller is not installed")
        sys.exit(1)
    else:
        print("pyinstaller is installed, proceeding...")

    clean()

    print("Creating pyinstaller dist")
    if create_pyinstaller_dist() != 0:
        print("Error during pyinstaller execution")
        sys.exit(1)
    else:
        print("Created dist with pyinstaller")

    create_installer_folders()
    copy_files()
    create_deb_package()


if __name__ == "__main__":
    main()
