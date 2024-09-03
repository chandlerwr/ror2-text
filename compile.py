import json
import os


def check_new_keys():
    """Check for new language keys in en/output.json versus keys.json."""

    keys = set()
    with open('keys.json') as f:
        keys.update(json.load(f)['keys'])

    output = set()
    with open('en/output.json', encoding="utf-8-sig") as f:
        output.update(json.load(f)['strings'].keys())

    diff = output - keys
    if len(diff) > 0:
        print(f"Failed to find the following {len(diff)} language keys in keys.json:")
        for k in diff:
            print(k)
        return False
    else:
        print("keys.json is up to date.")
        return True


def save_keys():
    """Save all the language keys from en/output.json to keys.json."""

    with open('en/output.json', encoding="utf-8-sig") as f:
        all = json.load(f)
        with open('keys.json', 'w') as key_file:
            json.dump({'keys': list(all['strings'].keys())}, key_file)


def check_files():
    """Check the language files in files/ against keys.json."""
    
    # Load keys file
    keys = set()
    with open('keys.json') as f:
        keys.update(json.load(f)['keys'])
    print(f"keys.json had {len(keys)} keys.")

    for f in os.scandir('files'):
        if f.is_file():
            try:
                with open(f, encoding="utf-8-sig") as txt:
                    keys -= set(json.load(txt)['strings'].keys())
            except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                print(f"Failed to read '{f}'. Exiting...")
                exit()
    
    if len(keys) > 0:
        print(f"Failed to find the following {len(keys)} language keys in files:")
        for k in keys:
            print(k)
        return False
    else:
        print("Files are up to date.")
        return True


def compile_files():
    """Compile the language files in files/ into output.json."""
    strings = {}
    for f in os.scandir('files'):
        if f.is_file():
            with open(f, encoding="utf-8-sig") as txt:
                strings.update(json.load(txt)['strings'])
            print(f"Read '{f}', strings is now {len(strings)}")
    with open('output.json', 'w', encoding="utf-8-sig") as f:
        json.dump({'strings': strings}, f, indent=2)


if __name__ == "__main__":
    if not check_new_keys():
        exit()

    if not check_files():
        exit()

    compile_files()
    print("Saved files to output.json")