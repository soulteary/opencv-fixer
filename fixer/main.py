import subprocess
import os
from packaging import version
import site
import shutil


def AutoFix():
    # 1. Check if opencv is installed 
    cmdExist = subprocess.run(['pip', 'show', 'opencv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if cmdExist.stderr:
        return False
    # 2. Get the installed OpenCV version
    ver = ''
    for line in cmdExist.stdout.splitlines():
        if line.strip().startswith('Version:'):
            ver = line.split(': ')[1]
            break
    if not ver:
        return False
    # 3. Check whether the installed package version is newer than 4.9
    if version.parse(ver) >= version.parse("4.9"):
        return False
    # 4. Uninstall the installed opencv-python, keep meta clean
    opencv_packages = get_opencv_packages()
    if opencv_packages:
        print(f"Uninstalling the following OpenCV-related packages: {', '.join(opencv_packages)}")
        uninstall_packages(opencv_packages)
    # 5. If the version is lower than 4.9, print the version and prompt the user to upgrade
    print("Found opencv-python version is lower than 4.9, version="+ver)
    print("Begin upgrade your opencv-python version to 4.9+.")
    packagePath = os.path.join(site.getsitepackages()[0], 'cv2')
    try:
        if os.path.exists(packagePath):
            shutil.rmtree(packagePath)
            print(f"The folder {packagePath} has been removed successfully")
            # 6. After the removal is completed, install the latest version of opencv-python
            cmd = subprocess.run(['pip', 'install', 'opencv-python-headless'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if cmd.stderr:
                print(f"Install opencv-python-headless failed: {cmd.stderr}")
                return False
            print("Install opencv-python-headless successfully")
            # 7. Check whether the installation is successful
            cmd = subprocess.run(['python', '-c', '"import cv2; print(cv2.__version__)"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if cmd.stderr:
                print(f"Install opencv-python-headless failed: {cmd.stderr}")
                return False
            print(f"Install opencv-python-headless successfully, version={cmd.stdout}")
        return True
    except OSError as e:
        print(f"Remove: {packagePath} : {e.strerror}")
        return False

def get_opencv_packages():
    pip_list_output = subprocess.run(['pip', 'list', '--format=freeze'], capture_output=True, text=True)
    if pip_list_output.returncode != 0:
        print("Failed to list installed packages.")
        return []
    opencv_packages = [line.split('==')[0] for line in pip_list_output.stdout.split('\n') if 'opencv' in line.lower()]
    return opencv_packages

def uninstall_packages(packages):
    for package in packages:
        uninstall_output = subprocess.run(['pip', 'uninstall', '-y', package], capture_output=True, text=True)
        if uninstall_output.returncode == 0:
            print(f"Successfully uninstalled {package}")
        else:
            print(f"Failed to uninstall {package}")
            print(uninstall_output.stdout)
            print(uninstall_output.stderr)

if __name__ == "__main__":
    if AutoFix():
        print("Fixed successfully")
    else:
        print("It seems that your opencv-python version is higher than 4.9, no need to fix")
