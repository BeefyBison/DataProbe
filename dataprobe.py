"""Collects information about files for data directories in the last month."""
import os
import time

def get_folder_info(folder_path):
    """Collects information about files within a specified folder in the last month."""
    now = time.time()
    one_month_ago = now - (24 * 60 * 60 * 30)
    file_quantity = 0
    total_size = 0
    try:
        for item in os.scandir(folder_path):
            item_path = os.path.join(folder_path, item.name)
            if item.is_file():
                modified_time = os.path.getmtime(item_path)
                if modified_time >= one_month_ago:
                    file_quantity = file_quantity + 1
                    file_info = {
                        "name": item.name,
                        "size": os.path.getsize(item_path)
                    }
                    total_size = total_size + file_info["size"]
            elif item.is_dir():
                file_quantity = 0
                print(item_path + "\n")
                print("-"*30)
                get_folder_info(item)
        if file_quantity != 0:
            print(f"Average size is: {format_size(total_size/file_quantity)}")
            print(f"Quantity is: {file_quantity}")
            print(f"Total size is: {format_size(total_size)}")
            print(f"Expected size in a month: {format_size(total_size*30)}")
            print(f"Expected size in a year: {format_size(total_size*365)}")
    except ZeroDivisionError:
        print("")
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for '{folder_path}'.")

def format_size(size_in_bytes):
    """Converts bytes to human-readable format."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    if size_in_bytes < 1024**2:
        return f"{size_in_bytes / 1024:.2f} KB"
    if size_in_bytes < 1024**3:
        return f"{size_in_bytes / (1024**2):.2f} MB"
    return f"{size_in_bytes / (1024**3):.2f} GB"

if __name__ == "__main__":
    get_folder_info('/data/testdata')
