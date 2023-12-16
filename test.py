from dataclasses import dataclass
import os
import json
from pydantic import BaseModel


class Cake(BaseModel):
    username: str
    pkgname: str
    version: str

    def __hash__(self):
        return hash((self.username, self.pkgname, self.version))

class CakeMeta(BaseModel):
    cake: Cake
    deps: list[Cake]
    download: str

def scan_json_files(directory) -> dict[Cake, CakeMeta]:
    metas = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                print(f"Reading JSON file: {relative_path}")

                def extract_info(path) -> Cake:
                    """
                    test/D/0.1.4.json: (test, D, 0.1.4)
                    test/D/asdf/0.1.4.json: (test, D/asdf, 0.1.4)
                    """
                    path = path.replace("index/user/", "")
                    parts = path.split('/')
                    username = parts[0]
                    version = parts[-1].replace(".json", "")
                    pkgname = '/'.join(parts[1:-1])
                    return Cake(username=username, pkgname=pkgname, version=version)
                
                cake = extract_info(relative_path)
                # print(cake)
                
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        deps = [Cake(username=fullname.split('/', 1)[0], pkgname=fullname.split('/', 1)[1], version=version) for fullname, version in data['deps'].items()]
                        metas[cake] = CakeMeta(cake=cake, deps=deps, download=data['download'])
                except json.JSONDecodeError as e:
                    print(f"Error reading JSON file {file_path}: {e}")

    return metas

metas = scan_json_files(".")

for cake, meta in metas.items():
    # print(cake, meta)
    print(f"[{cake.username} {cake.pkgname} {cake.version}]: {meta.download}")

