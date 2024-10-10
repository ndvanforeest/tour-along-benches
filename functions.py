import os
import pickle
import subprocess


def run_process(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running osmium: {e.stderr}")


def write_to_pkl(fname: str, obj):
    with open(fname, "wb") as fp:
        pickle.dump(obj, fp, pickle.HIGHEST_PROTOCOL)


def read_from_pkl(fname: str):
    if os.path.exists(fname):
        with open(fname, "rb") as f:
            obj = pickle.load(f)
            return obj
    raise FileExistsError(f"{fname} does not exist.")
