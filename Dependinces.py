def main():
    from os import system

    modules = (
    "psutil",
    "gputil"
    )

    for module in modules:
        system(f"pip install {module}")