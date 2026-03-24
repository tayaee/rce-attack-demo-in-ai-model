import pickletools
import zipfile
import click


def sanity_check(file_path):
    results = []
    try:
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                pkl_files = [
                    name for name in zip_ref.namelist() if name.endswith(".pkl")
                ]
                if not pkl_files:
                    return False, "No pickle data found in archive."
                with zip_ref.open(pkl_files[0]) as f:
                    data = f.read()
        else:
            with open(file_path, "rb") as f:
                data = f.read()

        current_func = None
        for opcode, arg, pos in pickletools.genops(data):
            if opcode.name == "GLOBAL":
                module, name = arg.split()
                if name in ("system", "run", "eval", "exec", "popen", "spawn"):
                    current_func = f"{module}.{name}"

            elif opcode.name in ("STRING", "BINUNICODE") and current_func:
                results.append({"func": current_func, "payload": arg, "pos": pos})
                current_func = None

        return True, results
    except Exception as e:
        return False, str(e)


@click.command()
@click.option("--pth-file", required=True, help="Path to the PyTorch model file (.pth)")
def main(pth_file):
    print(f"[!] Running sanity check on '{pth_file}'...")
    print("-" * 50)

    success, output = sanity_check(pth_file)

    if not success:
        print(f"[ERROR] Analysis failed: {output}")
        return

    if not output:
        print("[SAFE] No immediate RCE payloads detected.")
    else:
        for entry in output:
            print("[DANGER] Malicious Execution Found:")
            print(f"  >>> {entry['func']}('{entry['payload']}')")
            print(f"  (Detected at position {entry['pos']})")
            print("-" * 50)


if __name__ == "__main__":
    main()
