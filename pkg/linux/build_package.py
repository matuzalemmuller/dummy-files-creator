#! /usr/bin/env python3
import configparser
import os
import pathlib
import shutil
import subprocess
import sys


LINUX_SPEC_DIR = f"{pathlib.Path(__file__).parent.absolute()}"
DESKTOP_FILE = f"{LINUX_SPEC_DIR}/var/dummy-files-creator.desktop"
ICON_FILE = f"{LINUX_SPEC_DIR}/../../design/icon/icon.svg"
DIST_PATH = f"{LINUX_SPEC_DIR}/dist"
BUILD_PATH = f"{LINUX_SPEC_DIR}/build"
LOGS_PATH = f"{LINUX_SPEC_DIR}/logs"
PKG_PATH = f"{LINUX_SPEC_DIR}/package"
PKG_DESKTOP_PATH = f"{PKG_PATH}/usr/share/applications"
PKG_ICON_PATH = f"{PKG_PATH}/usr/share/icons/hicolor/scalable/apps"
PKG_OPT_PATH = f"{PKG_PATH}/opt"


def clean_workspace(package_extension: str):
    print("Cleaning workspace...", end=" ", flush=True)

    if os.path.exists(f"{LINUX_SPEC_DIR}/dummyfilescreator.{package_extension}"):
        try:
            os.remove(f"{LINUX_SPEC_DIR}/dummyfilescreator.{package_extension}")
        except OSError as error:
            print(f"error: {error}")
            return False

    if os.path.isdir(DIST_PATH):
        try:
            shutil.rmtree(DIST_PATH)
        except (shutil.Error, OSError) as error:
            print(f"error: {error}")
            return False

    if os.path.isdir(BUILD_PATH):
        try:
            shutil.rmtree(BUILD_PATH)
        except (shutil.Error, OSError) as error:
            print(f"error: {error}")
            return False

    if os.path.isdir(PKG_PATH):
        try:
            shutil.rmtree(PKG_PATH)
        except (shutil.Error, OSError) as error:
            print(f"error: {error}")
            return False

    print("cleaned workspace")

    return True


def is_program_installed(program_name: str):
    print(f"Checking if {program_name} is installed...", end=" ", flush=True)
    if shutil.which(program_name):
        print(f"{program_name} is installed")
        return True
    print(f"{program_name} not installed (or not added to $PATH)")

    return False


def create_pyinstaller_dist():
    print("Creating pyinstaller dist...", end=" ", flush=True)

    try:
        with open(f"{LOGS_PATH}/pyinstaller.log", "w") as f:
            cmd = subprocess.call(
                [
                    "pyinstaller",
                    f"{LINUX_SPEC_DIR}/linux.spec",
                    "--distpath",
                    DIST_PATH,
                    "--workpath",
                    BUILD_PATH,
                ],
                stdout=f,
                stderr=f,
            )
            if cmd != 0:
                print(f"error: see {LINUX_SPEC_DIR}/logs/pyinstaller.log for details")
                return False
    except IOError as error:
        print(f"error: {error}")
        return False

    print("created dist with pyinstaller")

    return True


def create_log_folder():
    print("Creating log folder...", end=" ", flush=True)

    if os.path.isdir(LOGS_PATH):
        try:
            shutil.rmtree(LOGS_PATH)
        except (shutil.Error, OSError) as error:
            print(f"error: {error}")
            return False

    try:
        os.makedirs(LOGS_PATH)
    except OSError as error:
        print(f"error: {error}")
        return False

    print("log folder created")

    return True


def create_linux_package(package_extension: str):
    print(f"Creating {package_extension} package...", end=" ", flush=True)

    cmplt_proc = subprocess.run(
        [
            "find",
            f"{PKG_OPT_PATH}/dummyfilescreator",
            "-type",
            "f",
            "-exec",
            "chmod",
            "644",
            "--",
            "{}",
            "+",
        ],
        capture_output=True,
    )

    if cmplt_proc.returncode != 0:
        print(f"error: {cmplt_proc.stderr.decode()}")
        return False

    cmplt_proc = subprocess.run(
        [
            "find",
            PKG_OPT_PATH + "/dummyfilescreator",
            "-type",
            "d",
            "-exec",
            "chmod",
            "755",
            "--",
            "{}",
            "+",
        ],
        capture_output=True,
    )

    if cmplt_proc.returncode != 0:
        print(f"error: {cmplt_proc.stderr.decode()}")
        return False

    cmplt_proc = subprocess.run(
        [
            "find",
            f"{PKG_PATH}/usr/share",
            "-type",
            "f",
            "-exec",
            "chmod",
            "644",
            "--",
            "{}",
            "+",
        ],
        capture_output=True,
    )

    if cmplt_proc.returncode != 0:
        print(f"error: {cmplt_proc.stderr.decode()}")
        return False

    cmplt_proc = subprocess.run(
        [
            "chmod",
            "+x",
            f"{PKG_OPT_PATH}/dummyfilescreator/dummy-files-creator",
        ],
        capture_output=True,
    )

    if cmplt_proc.returncode != 0:
        print(f"error: {cmplt_proc.stderr.decode()}")
        return False

    config = configparser.ConfigParser()
    config.read(f"{LINUX_SPEC_DIR}/../../package.ini")

    if not config.has_section("Info"):
        print(f"error: missing Info section/invalid {LINUX_SPEC_DIR}/../../package.ini")
        return False

    cmplt_proc = subprocess.run(
        [
            "fpm",
            "-C",
            PKG_PATH,
            "-s",
            "dir",
            "-t",
            package_extension,
            "-n",
            "dummyfilescreator",
            "--vendor",
            "",
            "--deb-priority",
            "optional",
            "-v",
            config["Info"]["version"],
            "--license",
            config["Info"]["license"],
            "-m",
            config["Info"]["author"],
            "--url",
            config["Info"]["url"],
            "--description",
            config["Info"]["description"],
            "-p",
            f"{LINUX_SPEC_DIR}/dummyfilescreator.{package_extension}",
        ],
        capture_output=True,
    )

    if cmplt_proc.returncode != 0:
        print(f"error: {cmplt_proc.stderr.decode()}")
        return False

    print(f"created {LINUX_SPEC_DIR}/dummyfilescreator.{package_extension}")

    return True


def create_installer_folders():
    print("Creating package folders...", end=" ", flush=True)

    try:
        os.makedirs(PKG_DESKTOP_PATH)
        os.makedirs(PKG_ICON_PATH)
    except OSError as error:
        print(f"error: {error}")
        return False

    print("package folders created")

    return True


def copy_files():
    print("Copying files to package folder...", end=" ", flush=True)

    try:
        shutil.copy(DESKTOP_FILE, PKG_DESKTOP_PATH)
        shutil.copy(ICON_FILE, f"{PKG_ICON_PATH}/dummy-files-creator.svg")
        shutil.copytree(DIST_PATH, PKG_OPT_PATH)
    except (shutil.Error, OSError) as error:
        print(f"error: {error}")
        return False

    print("files copied")

    return True


def main():
    if not is_program_installed("ruby"):
        sys.exit(1)

    if not is_program_installed("fpm"):
        sys.exit(1)

    if not is_program_installed("pyinstaller"):
        sys.exit(1)

    if is_program_installed("dpkg"):
        package_extension = "deb"
    elif is_program_installed("rpm"):
        package_extension = "rpm"
    else:
        sys.exit(1)

    if not clean_workspace(package_extension):
        sys.exit(1)

    if not create_log_folder():
        sys.exit(1)

    if not create_pyinstaller_dist():
        sys.exit(1)

    if not create_installer_folders():
        sys.exit(1)

    if not copy_files():
        sys.exit(1)

    if not create_linux_package(package_extension):
        sys.exit(1)


if __name__ == "__main__":
    main()
