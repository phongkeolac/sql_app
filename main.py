import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, simpledialog
import duckdb
from tabulate import tabulate
import os
import glob # Để tìm kiếm file theo pattern

# Cau hinh ung dung
# Đảm bảo thư mục data tồn tại cho việc lưu trữ cơ sở dữ liệu
DATBASE_DIR = "data"
DEFAULT_DB_FILE = "default.duckdb"
MEMORY_DB_NAME = ":memory"


if not os.path.exists(DATBASE_DIR):
    os.makedirs(DATBASE_DIR)

class DuckDBManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Database Desktop Manager")
        master.geometry("1000x700") # Kich thuoc cua so mac dinh
        master.configure(bg='#282c34')

        self.db_conn = None
        self.current_db_path = ""
        self.connect_to_default_db()

        # Config Styles/Fonts
        self.monospace_font = ('Consolas', 10) # Font cua terminal
        self.header_font = ('Consolas', 12, 'bold')
        self.text_color = '#abb2bf' # Màu chữ
        self.bg_color = '#282c34'   # Màu nền chính
        self.widget_bg_color = '#21252b' # Màu nền cho các widget input/output
        self.button_color = '#61afef' # Màu nút
        self.button_fg_color = 'white' # Màu chữ nút
        self.active_button_color = '#569cd6' # Màu nút khi hover

        # Main PainWindow (Sidebar va Maincontent)
        self.main_pane = tk.PanedWindow(master, orient=tk.HORIZONTAL, bg=self.bg_color)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # sidebar frame (left)
        self.sidebar_frame = tk.Frame(self.main_pane, bg=self.bg_color, width=250)
        self.main_pane.add(self.sidebar_frame, minsize=180)

        # Main content frame (right)
        self.content_frame = tk.Frame(self.main_pane, bg=self.bg_color)
        self.main_pane.add(self.content_frame, minsize=400)

        self._setup_sidebar()
        self._setup_main_content()

        # Load danh sach database khi khoi dong
        self._load_database_list()
    def connect_to_default_db(self):
        default_db_file_path = os.path.join(DATBASE_DIR, DEFAULT_DB_FILE)
        if not os.path.exists(default_db_file_path):
            try:
                temp_conn = duckdb.connect(database=default_db_file_path)
                temp_conn.close()
                self._append_output(f'Đã tạo file Database mặc định: {DEFAULT_DB_FILE}')
            except Exception as e:
                self._append_output(f"Không thể tạo database mặc định '{DEFAULT_DB_FILE}': {e}")
                self._connect_to_db(MEMORY_DB_NAME)
                return
        self._connect_to_db(default_db_file_path)
    
    def _setup_sidebar(self):
        # Header
        tk.Label(self.sidebar_frame, text="DUCKDB DATABASES", font=self.header_font, fg='#e06c75', bg=self.bg_color, pady=5) \
        .pack(fill=tk.X, padx=5, pady=(5,0))

        # Current DB Info
        self.current_db_label = tk.Label(self.sidebar_frame, text="Current DB: N/A", font=self.monospace_font, fg='#98c379', bg=self.bg_color, anchor='w')
        self.current_db_label.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Listbox hiển thị danh sách db
        db_list_frame = tk.Frame(self.sidebar_frame, bg=self.widget_bg_color)
        db_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.db_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.db_listbox.bind("<<ListboxSelect>>", self._on_db_selected)

        # Scrollbar cho listbox
        listbox_scrollbar = tk.Scrollbar(db_list_frame, orient=tk.VERTICAL, command=self.db_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.db_listbox.config(yscrollcommand=listbox_scrollbar.set)

        # Nút chức năng DB
        button_frame = tk.Frame(self.sidebar_frame, bg=self.bg_color, pady=5)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(button_frame, text="Tạo DB Mới", command=self._create_new_db, bg=self.button_color, fg=self.button_fg_color, relief=tk.FLAT, font=self.monospace_font) \
            .pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Tải Lại DBs", command=self._load_database_list, bg=self.button_color, fg=self.button_fg_color, relief=tk.FLAT, font=self.monospace_font) \
            .pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Xóa DB Chọn", command=self._delete_selected_db, bg='#e06c75', fg=self.button_fg_color, relief=tk.FLAT, font=self.monospace_font) \
            .pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Thoát App", command=self.master.quit, bg='#abb2bf', fg=self.button_fg_color, relief=tk.FLAT, font=self.monospace_font) \
            .pack(fill=tk.X, pady=2)

if __name__ == "__main__":
    pass
