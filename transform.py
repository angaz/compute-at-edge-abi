import re
import sys
import pathlib


def wrap_module(name: str, witx: str) -> str:
    out = f"(module ${name}\n"
    
    out += "\n".join([
        "    " + line if len(line) > 0 else ""
        for line in witx.splitlines()
    ])

    out += "\n)\n"

    return out


def transform_cache_file(cache_file: str) -> str:
    before_module = ""

    with open(cache_file) as f:
        while True:
            line = f.readline()

            if line == "(module $fastly_cache\n":
                witx = (
                    line +
                    "    (resource $cache_handle_res)\n\n" +
                    before_module +
                    "\n" +
                    f.read()
                )
                witx = witx.replace(
                    "(typename $cache_handle (handle))",
                    "(typename $cache_handle (handle $cache_handle_res))",
                )

                return witx

            before_module += "    " + line


def transform_config_store_file(config_store_file: str) -> str:
    before_module = ""

    with open(config_store_file) as f:
        while True:
            line = f.readline()

            if line == "(module $fastly_config_store\n":
                witx = (
                    line +
                    "    (resource $config_store_handle_res)\n" +
                    before_module +
                    "\n" +
                    f.read()
                )
                witx = witx.replace(
                    "(typename $config_store_handle (handle))",
                    "(typename $config_store_handle (handle $config_store_handle_res))",
                )

                return witx

            before_module += "    " + line


def transform_typenames_file(typenames_file: str) -> str:
    with open(typenames_file) as f:
        witx = (
            f.readline() +
            "(resource $http_handle)\n\n" +
            f.read()
        )

        witx = witx.replace(
            "(handle)",
            "(handle $http_handle)",
        )

        return wrap_module("typenames", witx)


def import_file(match: re.Match):
    witx_file = match.group(1)
    name = match.group(2).replace("-", "_")

    if name == "cache":
        return transform_cache_file(witx_file)

    if name == "config_store":
        return transform_config_store_file(witx_file)

    if name == "typenames":
        return transform_typenames_file(witx_file)

    with open(witx_file) as f:
        return wrap_module(name, f.read())


def split_modules(witx: str, modules_dir: pathlib.Path):
    modules_dir.mkdir(0o755, parents=True, exist_ok=True)

    module_lines = []
    module_name = ""

    for line in witx.splitlines():
        if line.startswith("(module $"):
            if line[9:] == "typenames":
                module_lines = [line]
            else:
                module_lines = [line, "    (use * from $typenames)\n"]

            module_name = line[9:] + ".witx"

            print(module_name)

            continue

        if len(module_lines) > 0:
            module_lines.append(line)

            if line == ")":
                with open(modules_dir / module_name, "w") as f:
                    f.write("\n".join(module_lines) + "\n")

                module_lines = []


def transform_witx(base_file: str):
    with open(base_file) as f:
        witx = f.read()

    while True:
        witx, n = re.subn(r'\(use "((.*?)\.witx)"\)', import_file, witx)

        if n == 0:
            break

    split_modules(witx, pathlib.Path("witx"))


def main():
    base_file = sys.argv[1]

    transform_witx(base_file)


if __name__ == "__main__":
    main()
