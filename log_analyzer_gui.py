import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import tkinter.font as tkFont
import os
import re
import threading
from collections import defaultdict
from datetime import datetime
import csv
import sys

# ========== Parsing ==========
def parse_datetime_from_line(line):
    match = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
    if match:
        try:
            return datetime.strptime(match.group(0), '%Y-%m-%d %H:%M:%S')
        except:
            return None
    return None

def get_all_datetimes(files, update_status=None):
    datetimes = set()
    for idx, file_path in enumerate(files):
        if update_status:
            update_status(os.path.basename(file_path))
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    dt = parse_datetime_from_line(line)
                    if dt:
                        datetimes.add(dt.strftime('%Y-%m-%d %H:%M:%S'))
        except:
            continue
    return sorted(datetimes)

# ========== Analyze ==========
def analyze_logs(files, keyword, start_dt=None, end_dt=None, mode="count", update_status=None, stop_flag=None):
    results = defaultdict(lambda: defaultdict(list))
    pattern = re.compile(re.escape(keyword.strip()), re.IGNORECASE)

    for idx, file_path in enumerate(files):
        if stop_flag and stop_flag[0]:
            break

        filename = os.path.basename(file_path)
        if update_status:
            update_status(filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if pattern.search(line):
                        timestamp = parse_datetime_from_line(line)
                        if timestamp:
                            if start_dt and timestamp < start_dt:
                                continue
                            if end_dt and timestamp > end_dt:
                                continue
                            date = timestamp.strftime('%Y-%m-%d')
                        else:
                            date = "Unknown"

                        if mode == "count":
                            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                            ip = ip_match.group(1) if ip_match else "Unknown IP"
                            key = f"{date} | {ip}"
                            results[filename][key].append(1)
                        else:
                            results[filename][date].append(line.strip())
        except:
            results[filename]["Error"].append("Error reading file")
    return results

# ========== GUI ==========
def show_progress_window(msg="Processing..."):
    progress_win = tk.Toplevel(root)
    progress_win.title("Processing")
    progress_win.geometry("400x150")
    progress_win.resizable(False, False)
    progress_win.grab_set()

    frame = tk.Frame(progress_win, padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    label = tk.Label(frame, text=msg)
    label.pack(pady=(0, 10))

    pb = ttk.Progressbar(frame, mode='indeterminate', length=300)
    pb.pack()
    pb.start(10)

    status_label = tk.Label(frame, text="")
    status_label.pack(pady=(10, 0))

    cancel_button = tk.Button(frame, text="Cancel")
    cancel_button.pack(pady=(10, 0))

    progress_win.update()
    return progress_win, pb, status_label, cancel_button

def select_files():
    global selected_files
    progress_win, pb, status_label, cancel_button = show_progress_window("Importing files...")
    stop_flag = [False]

    def update_status(filename):
        status_label.config(text=f"Reading: {filename}")
        status_label.update_idletasks()

    def load_thread():
        files = filedialog.askopenfilenames(
            title="Select log files",
            filetypes=[("Log files", "*.txt *.log"), ("All files", "*.*")]
        )
        if not files:
            result_var.set("⚠️ No files selected.")
            pb.stop()
            progress_win.destroy()
            return

        selected_files[:] = list(files)
        all_dt = get_all_datetimes(selected_files, update_status)
        if not all_dt:
            result_var.set("⚠️ No valid datetime entries found.")
        else:
            start_dt_cb['values'] = all_dt
            end_dt_cb['values'] = all_dt
            start_dt_cb.set(all_dt[0])
            end_dt_cb.set(all_dt[-1])
            result_var.set(f"✅ Loaded {len(files)} files with {len(all_dt)} datetime entries.")

        pb.stop()
        progress_win.destroy()

    cancel_button.config(command=lambda: stop_flag.__setitem__(0, True))
    threading.Thread(target=load_thread).start()

def run_analysis():
    if not selected_files:
        result_var.set("⚠️ Please select log files.")
        return

    keyword = keyword_entry.get().strip()
    if not keyword:
        result_var.set("⚠️ Please enter a keyword to search.")
        return

    try:
        start_dt = datetime.strptime(start_dt_cb.get(), '%Y-%m-%d %H:%M:%S')
        end_dt = datetime.strptime(end_dt_cb.get(), '%Y-%m-%d %H:%M:%S')
    except:
        result_var.set("⚠️ Invalid datetime.")
        return

    progress_win, pb, status_label, cancel_button = show_progress_window("Analyzing logs...")
    stop_flag = [False]

    def update_status(text):
        status_label.config(text=f"Reading: {text}")
        status_label.update_idletasks()

    def analyze_thread():
        global latest_results
        mode = mode_var.get()
        latest_results = analyze_logs(selected_files, keyword, start_dt, end_dt, mode, update_status, stop_flag)

        pb.stop()
        progress_win.destroy()
        match_listbox.delete(0, tk.END)
        for file, by_key in latest_results.items():
            match_listbox.insert(tk.END, f"File: {file}")
            for key, entries in by_key.items():
                if mode == "count":
                    match_listbox.insert(tk.END, f"  {key}: {len(entries)} matches")
                else:
                    for line in entries:
                        match_listbox.insert(tk.END, f"[{file} | {key}] {line[:100]}")

    cancel_button.config(command=lambda: stop_flag.__setitem__(0, True))
    threading.Thread(target=analyze_thread).start()

def reset_all():
    global selected_files, latest_results
    selected_files = []
    latest_results = {}
    keyword_entry.delete(0, tk.END)
    start_dt_cb.set('')
    end_dt_cb.set('')
    start_dt_cb['values'] = []
    end_dt_cb['values'] = []
    match_listbox.delete(0, tk.END)
    result_var.set("🔁 Reset complete.")

def export_csv():
    if not latest_results:
        messagebox.showinfo("No Data", "Please analyze first.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not path:
        return

    try:
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if mode_var.get() == "count":
                writer.writerow(["File", "Date + IP", "Match Count"])
                for file, by_day in latest_results.items():
                    for key, entries in by_day.items():
                        writer.writerow([file, key, len(entries)])
            else:
                writer.writerow(["File", "Date", "Line"])
                for file, by_day in latest_results.items():
                    for date, lines in by_day.items():
                        for line in lines:
                            writer.writerow([file, date, line])
        messagebox.showinfo("Export", f"✅ Exported to:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Export failed:\n{e}")

# GUI
root = tk.Tk()
if getattr(sys, 'frozen', False):
    # กรณีรันจาก exe
    try:
        root.iconbitmap(sys._MEIPASS + '/icon.ico')
    except:
        pass
else:
    try:
        root.iconbitmap('icon.ico')
    except:
        pass

root.title("Log Analyzer")
root.geometry("850x700")

if "Comic Sans MS" in tkFont.families():
    root.option_add("*Font", ("Comic Sans MS", 10))

selected_files = []
latest_results = {}
mode_var = tk.StringVar(value="count")

header = tk.Label(root, text="🧠 Log Analyzer", font=("Comic Sans MS", 18, "bold"))
header.pack(pady=(10, 5))

tk.Button(root, text="📂 Browse Files", command=select_files).pack(pady=5)

# Keyword entry
keyword_label = tk.Label(root, text="Keyword:")
keyword_label.pack()
keyword_entry = tk.Entry(root, width=40)
keyword_entry.pack(pady=(0, 5))

mode_frame = tk.Frame(root)
tk.Radiobutton(mode_frame, text="Count", variable=mode_var, value="count").pack(side="left", padx=10)
tk.Radiobutton(mode_frame, text="Show", variable=mode_var, value="show").pack(side="left", padx=10)
mode_frame.pack(pady=5)

dt_frame = tk.Frame(root)
tk.Label(dt_frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
start_dt_cb = ttk.Combobox(dt_frame, width=25, state="readonly")
start_dt_cb.grid(row=0, column=1, padx=5)
tk.Label(dt_frame, text="End Date:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
end_dt_cb = ttk.Combobox(dt_frame, width=25, state="readonly")
end_dt_cb.grid(row=1, column=1, padx=5)
dt_frame.pack(pady=10)

btn_frame = tk.Frame(root)
tk.Button(btn_frame, text="🔍 Analyze", command=run_analysis).pack(side="left", padx=10)
tk.Button(btn_frame, text="📤 Export CSV", command=export_csv).pack(side="left", padx=10)
tk.Button(btn_frame, text="🔁 Reset", command=reset_all).pack(side="left", padx=10)
btn_frame.pack(pady=5)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, justify="left", fg="darkblue", wraplength=800).pack(pady=10)

match_listbox = tk.Listbox(root, width=110, height=20)
match_listbox.pack(pady=10)

root.mainloop()
