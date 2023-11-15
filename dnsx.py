import pip
from packaging import version


def check_latest_version(package_name):
    installed_version = None
    try:
        installed_version = pip.__version__
        package = __import__(package_name)
        if hasattr(package, '__version__'):
            installed_version = package.__version__
        elif hasattr(package, 'version'):
            installed_version = package.version
    except ImportError:
        pass
    
    if installed_version:
        latest_version = pip._vendor.packaging.version.parse(
            pip._internal.utils.misc.get_installed_version(package_name)
        )
        print(f"Installed version of {package_name}: {installed_version}")
        print(f"Latest version of {package_name}: {latest_version}")
    else:
        print(f"Could not find {package_name} installed.")

# Example usage:
check_latest_version('numpy')