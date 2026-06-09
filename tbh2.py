import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import shutil

class TaskbarHeroMultiPatcher:
    def __init__(self, root):
        self.root = root
        self.root.title("\u26A1 TBH Stable Menu Mod ver.(1.00.11) \u26A1")
        self.root.geometry("660x720")
        self.root.configure(bg="#0a0a0f")
        
        self.dll_path = "GameAssembly.dll"
        self.rainbow_hue = 0
        
        # Kept ONLY the verified working codes from your dump file
        self.patches = {
            "gold_val": {
                "name": "Unlimited Gold (ue.sv.ikv - Offset: 89222A)",
                "offsets": [0x89222A],
                "patch_bytes": [bytes.fromhex("48 C7 C2 00 CA 9A 3B")]
            },
            "gold_prot": {
                "name": "Gold Crash Protection (ue.sv.ikv + 13 - Offset: 892237)",
                "offsets": [0x892237],
                "patch_bytes": [bytes.fromhex("EB")]
            },
            "monsters_5k": {
                "name": "Spawn 5K Monsters (Offset: 946830)",
                "offsets": [0x946830],
                "patch_bytes": [bytes.fromhex("B8 88 13 00 00 C3")]
            },
            "monsters_10k": {
                "name": "Spawn 10K Monsters (Offset: 946830)",
                "offsets": [0x946830],
                "patch_bytes": [bytes.fromhex("B8 10 27 00 00 C3")]
            },
            "offline_xp": {
                "name": "Offline XP Multiplier (1 Billion - Offset: 8CACE0)",
                "offsets": [0x8CACE0],
                "patch_bytes": [bytes.fromhex("B8 28 6B 6E 4E 66 0F 6E C0 C3")]
            },
            "dlc_unlock": {
                "name": "DLC Unlocker + Unlock All Pets",
                "offsets": [0xB795C0, 0x94CB70],
                "patch_bytes": [bytes.fromhex("B8 01 00 00 00 C3"), bytes.fromhex("B8 01 00 00 00 C3")]
            }
        }
        
        self.vars = {key: tk.BooleanVar() for key in self.patches.keys()}
        self.create_widgets()
        self.update_rainbow_border()
 
    def create_widgets(self):
        self.border_frame = tk.Frame(self.root, bg="#f3e03b", bd=4)
        self.border_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_container = tk.Frame(self.border_frame, bg="#0a0a0f")
        self.main_container.pack(fill="both", expand=True)
        
        self.skull_overlay = tk.Frame(self.main_container, bg="#0a0a0f")
        self.skull_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        skull_pattern = "\U0001F480  " * 16
        for i in range(25):
            lbl_skull = tk.Label(
                self.skull_overlay, text=skull_pattern, 
                font=("Arial", 10), fg="#18181f", bg="#0a0a0f", anchor="w"
            )
            lbl_skull.pack(fill="x", pady=2)

        self.content_frame = tk.Frame(self.main_container, bg="")
        self.content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.content_frame.configure(bg="#0a0a0f")
        self.content_frame.lift()
        
        title = tk.Label(self.content_frame, text="\u26A1 ToBeHonest Sur Panel \u26A1", font=("Courier New", 15, "bold"), fg="#f3e03b", bg="#0a0a0f")
        title.pack(pady=15)
        
        self.status_label = tk.Label(self.content_frame, text="Status: Waiting for file selection...", font=("Arial", 9, "italic"), fg="#ff5555", bg="#0a0a0f")
        self.status_label.pack(pady=2)
        
        self.btn_select = tk.Button(
            self.content_frame, text="LOCATE GAMEASSEMBLY.DLL", command=self.select_dll, 
            bg="#f3e03b", fg="#0a0a0f", activebackground="#c6b630", activeforeground="#0a0a0f",
            font=("Arial", 9, "bold"), padx=10, pady=4, bd=0, cursor="hand2"
        )
        self.btn_select.pack(pady=8)
        
        frame_options = tk.LabelFrame(
            self.content_frame, text=" Select modifications to deploy ", 
            font=("Arial", 10, "bold"), fg="#f3e03b", bg="#111116", bd=1, labelanchor="n"
        )
        frame_options.pack(pady=10, fill="both", expand=True, padx=25)
        
        monster_keys = ["monsters_5k", "monsters_10k"]
        
        for key in self.patches.keys():
            if key in monster_keys:
                cb = tk.Checkbutton(
                    frame_options, text=self.patches[key]["name"], variable=self.vars[key],
                    command=lambda k=key: self.enforce_single_selection(k, monster_keys),
                    font=("Arial", 10), fg="#e0e0e0", bg="#111116", 
                    activebackground="#111116", activeforeground="#f3e03b", selectcolor="#0a0a0f"
                )
            else:
                cb = tk.Checkbutton(
                    frame_options, text=self.patches[key]["name"], variable=self.vars[key],
                    font=("Arial", 10), fg="#e0e0e0", bg="#111116", 
                    activebackground="#111116", activeforeground="#f3e03b", selectcolor="#0a0a0f"
                )
            cb.pack(anchor="w", pady=4, padx=10)
            
        self.lbl_info1 = tk.Label(frame_options, text="\u2139 Mod edits are written directly to local files. Keep the game completely closed when patching.", font=("Arial", 8, "italic"), fg="#f3e03b", bg="#111116")
        self.lbl_info1.pack(anchor="w", pady=6, padx=15)

        btn_frame = tk.Frame(self.content_frame, bg="#0a0a0f")
        btn_frame.pack(pady=15)

        self.btn_apply = tk.Button(
            btn_frame, text="APPLY SELECTED MODS", command=self.apply_patches, 
            bg="#f3e03b", fg="#0a0a0f", font=("Arial", 11, "bold"), padx=15, pady=8, state="disabled", bd=0
        )
        self.btn_apply.pack(side="left", padx=10)

        self.btn_revert = tk.Button(
            btn_frame, text="REVERT TO ORIGINAL", command=self.revert_dll, 
            bg="#22222a", fg="#ff5555", font=("Arial", 11, "bold"), padx=15, pady=8, state="disabled", bd=0
        )
        self.btn_revert.pack(side="left", padx=10)
 
    def update_rainbow_border(self):
        self.rainbow_hue = (self.rainbow_hue + 2) % 360
        h = self.rainbow_hue / 60.0
        x = int(255 * (1 - abs((h % 2) - 1)))
        
        if 0 <= h < 1: r, g, b = 255, x, 0
        elif 1 <= h < 2: r, g, b = x, 255, 0
        elif 2 <= h < 3: r, g, b = 0, 255, x
        elif 3 <= h < 4: r, g, b = 0, x, 255
        elif 4 <= h < 5: r, g, b = x, 0, 255
        else: r, g, b = 255, 0, x
        
        rainbow_hex = f"#{r:02x}{g:02x}{b:02x}"
        self.border_frame.configure(bg=rainbow_hex)
        self.root.after(40, self.update_rainbow_border)

    def enforce_single_selection(self, clicked_key, grouping):
        if self.vars[clicked_key].get():
            for key in grouping:
                if key != clicked_key:
                    self.vars[key].set(False)
 
    def select_dll(self):
        path = filedialog.askopenfilename(filetypes=[("Dynamic Link Library", "*.dll")])
        if path:
            if os.path.basename(path) == "GameAssembly.dll":
                self.dll_path = path
                self.detect_dll()
 
    def detect_dll(self):
        if os.path.exists(self.dll_path):
            self.status_label.config(text=f"DLL Identified: {os.path.basename(self.dll_path)}", fg="#f3e03b")
            self.btn_apply.config(state="normal")
            
            backup = self.dll_path + ".bak"
            if os.path.exists(backup):
                self.btn_revert.config(state="normal")
        else:
            self.status_label.config(text="Status: GameAssembly.dll file not detected.", fg="#ff5555")
            self.btn_apply.config(state="disabled")
            self.btn_revert.config(state="disabled")
 
    def apply_patches(self):
        if not os.path.exists(self.dll_path):
            return
            
        backup = self.dll_path + ".bak"
        if not os.path.exists(backup):
            shutil.copy2(self.dll_path, backup)
            self.btn_revert.config(state="normal")
            
        try:
            shutil.copy2(backup, self.dll_path)
            
            with open(self.dll_path, "r+b") as f:
                for key, p in self.patches.items():
                    if self.vars[key].get():
                        for idx, offset in enumerate(p["offsets"]):
                            f.seek(offset)
                            f.write(p["patch_bytes"][idx])
                            
            messagebox.showinfo("Success!", "All stable features successfully built into GameAssembly.dll!")
        except PermissionError:
            messagebox.showerror("Access Error", "Permission Denied: Close your game before writing patches!")
        except Exception as e:
            messagebox.showerror("Error", f"Binary stream failure: {str(e)}")

    def revert_dll(self):
        backup = self.dll_path + ".bak"
        if not os.path.exists(backup):
            messagebox.showerror("Error", "Backup file (.bak) not found!")
            return
            
        try:
            shutil.copy2(backup, self.dll_path)
            for key in self.vars.keys():
                self.vars[key].set(False)
                
            messagebox.showinfo("Restored!", "Game files successfully reverted back to original vanilla defaults.")
        except PermissionError:
            messagebox.showerror("Access Error", "Permission Denied: Close the game completely before running a restore!")
        except Exception as e:
            messagebox.showerror("Error", f"Restoration process failure: {str(e)}")
 
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskbarHeroMultiPatcher(root)
    root.mainloop()