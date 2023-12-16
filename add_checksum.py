import json
import hashlib
import requests
import sys

def add_checksum_to_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    download_url = data.get('download')
    if not download_url:
        raise ValueError("Download URL not found in JSON.")

    response = requests.get(download_url)
    checksum = hashlib.sha256(response.content).hexdigest()
    data['checksum'] = checksum

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 add_checksum.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    add_checksum_to_json(file_path)
