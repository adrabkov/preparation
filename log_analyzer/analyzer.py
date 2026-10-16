from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def get_log_files(folder_path):
    folder = Path(folder_path)
    path_list = []
    for path in folder.glob("*.log"):
        path_list.append(path)
    return path_list

def calc_log_lines(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder {folder} not found")

    if not folder.is_dir():
        raise NotADirectoryError(f"{folder} is not a directory") 
    
    count = 0
    levels = {}
    error_list = []

    for path in folder.glob("*.log"):
        try:
            with open(path, "r", encoding="utf-8") as file:
                if not file.readable():
                    continue
                for line in file:
                    record = parse_log_line(line)
                    if record is None:
                        continue
                    key = record["level"]

                    if key not in {"INFO", "WARNING", "ERROR"}:
                        continue
                    if key == "ERROR":
                        error_list.append(record["message"].rstrip())
                    levels[key] = levels.get(key, 0)+1
                    count +=1
        except PermissionError:
            print(f"No permission to read {path}")
            continue

        except UnicodeDecodeError:
            print(f"Can't decode {path}")

        except OSError as exc:
            print(f"Can't read {path}: {exc}")

    return {
        "total": count,
        "levels": levels,
        "last_errors": error_list[-5:]
    }

def parse_log_line(line):
    parts = line.split(maxsplit = 3)

    if len(parts) < 4:
        return None
    
    return {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": parts[2],
        "message": parts[3]
    }

# print(calc_log_lines("sample_logs"))



def read_log_file(path):
    path = Path(path)
    str_line = []

    try:
        with open(path, "r") as f:
            for line in f:
                str_line.append(line.rstrip())

    except FileNotFoundError:
        raise
    
    except PermissionError as exc:
        logging.warning(f"Permosiion denied: {exc}")
        return []
        
    return str_line

result = read_log_file("sample_logs/app2.log")
print(result)


def parse_lines(lines):
    result = []

    for line in lines:
        try:
            result.append(int(line))
        except ValueError as exc:
            logging.warning(f"Parsing error: {exc}")
            continue
    return result

def parse_log_line(line):
    parts = line.split(maxsplit=3)

    if len(parts) < 4:
        return None

    level = parts[2]
    if level not in {"INFO", "WARNING", "ERROR"}:
        return None 

    return {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": level,
        "message": parts[3],
    }
