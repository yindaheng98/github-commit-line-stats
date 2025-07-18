import os
import requests
import yaml
import re
vendor_url = "https://github.com/github-linguist/linguist/raw/refs/heads/main/lib/linguist/vendor.yml"
languages_url = "https://github.com/github-linguist/linguist/raw/refs/heads/main/lib/linguist/languages.yml"
vendors = yaml.safe_load(requests.get(vendor_url).text)
languages = yaml.safe_load(requests.get(languages_url).text)
extension_dict = {}
filename_dict = {}
for lang in languages:
    for ext in languages[lang].get("extensions", []):
        extension_dict[ext.lower()] = lang
    for filename in languages[lang].get("filenames", []):
        filename_dict[filename.lower()] = lang
vendor_list = []
for vendor in vendors:
    vendor_list.append(re.compile(vendor, re.IGNORECASE))


def get_language_by_filename(filename: str) -> str:
    lang = "unknown"
    if os.path.basename(filename).lower() in filename_dict:
        lang = filename_dict[os.path.basename(filename).lower()]
    if os.path.splitext(filename)[1].lower() in extension_dict:
        lang = extension_dict[os.path.splitext(filename)[1].lower()]
    if lang == "unknown":
        return "unknown"
    for vendor in vendor_list:
        if vendor.search(filename):
            return "vendor"
    return lang
