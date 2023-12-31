import shutil
from typing import List, Tuple
from pathlib import Path
from dataclasses import dataclass
import os
import json
from pydantic import BaseModel


class Cake(BaseModel):
    username: str
    pkgname: str

    def __eq__(self, other):
        return (self.username, self.pkgname) == (other.username, other.pkgname)

    def __hash__(self):
        return hash((self.username, self.pkgname))

class Version(BaseModel):
    version: str
    download: str
    deps: List[Tuple[str, str, str]] # (username, pkgname, version)

class Registry(BaseModel):
    cakes: dict[Cake, List[Version]]

def scan_json_files(directory) -> Registry:
    cakes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                print(f"Reading JSON file: {relative_path}")

                def extract_info(path) -> (str, str, str):
                    """
                    test/D/0.1.4.json: (test, D, 0.1.4)
                    test/D/asdf/0.1.4.json: (test, D/asdf, 0.1.4)
                    """
                    path = path.replace("index/user/", "")
                    parts = path.split('/')
                    username = parts[0]
                    version = parts[-1].replace(".json", "")
                    pkgname = '/'.join(parts[1:-1])
                    return username, pkgname, version
                
                username, pkgname, version = extract_info(relative_path)
                # print(cake)

                cake = Cake(username=username, pkgname=pkgname)
                if cake not in cakes:
                    cakes[cake] = []
                
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        deps = [(fullname.split('/', 1)[0], fullname.split('/', 1)[1], version) for fullname, version in data['deps'].items()]
                        print(data)
                        print(deps)
                        cakes[cake].append(Version(version=version, download=data["download"], deps=deps))
                except json.JSONDecodeError as e:
                    print(f"Error reading JSON file {file_path}: {e}")

    return Registry(cakes=cakes)

metas = scan_json_files(".")

# public dir
target_dir = Path("docs")
if target_dir.exists():
    shutil.rmtree(target_dir)
target_dir.mkdir(exist_ok=True)

# write index.md

ROOT_DIR = "option"

with open(target_dir / "index.md", "w") as f:
    f.write("# MoonCakes Index\n\n")

    for cake, versions in metas.cakes.items():
        f.write(f"* [{cake.username}/{cake.pkgname}](/{ROOT_DIR}/{cake.username}/{cake.pkgname}/)\n")

        # write index.md for each cake
        cake_dir = target_dir / cake.username / cake.pkgname
        cake_dir.mkdir(parents=True, exist_ok=True)
        with open(cake_dir / "index.md", "w") as f2:
            f2.write(f"# {cake.username}/{cake.pkgname}\n\n")
            f2.write("## Versions\n\n")
            for version in versions:
                f2.write(f"* [{version.version}](./{version.version}/)\n")
        
        # write index.md for each version
        for version in versions:
            version_dir = cake_dir / version.version
            version_dir.mkdir(parents=True, exist_ok=True)
            with open(version_dir / "index.md", "w") as f2:
                f2.write(f"# {cake.username}/{cake.pkgname} {version.version}\n\n")
                f2.write(f"Download: [{version.download}]({version.download})\n\n")
                f2.write("## Dependencies\n\n")
                for dep in version.deps:
                    f2.write(f"* [{dep[0]}/{dep[1]} {dep[2]}](/{ROOT_DIR}/{dep[0]}/{dep[1]}/{dep[2]}/)\n")

