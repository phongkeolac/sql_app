import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, simpledialog
import duckdb
from tabulate import tabulate
import os
import glob # Để tìm kiếm file theo pattern

# Cau hinh ung dung
# Đảm bảo thư mục data tồn tại cho việc lưu trữ cơ sở dữ liệu
DATBASE_DIR = "data"
DEFAULT_DF_FILE = "default.duckdb"
MEMORY_DB_NAME = ":memory"


if not os.path.exists(DATBASE_DIR):
    os.makedirs(DATBASE_DIR)

class DuckDBManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Database Desktop Manager")
        master.geometry("1000x700") # Kich thuoc cua so mac dinh
        master.configure(bg='#282c34')

if __name__ == "__main__":
    pass
