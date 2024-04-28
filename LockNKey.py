import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pyperclip
from cryptography.fernet import Fernet
import tkinter.ttk as ttk

def generate_key():
    # """
    # Generates a key for encryption and decryption.
    # """
    return Fernet.generate_key().decode()   

def copy_key():
    key_to_copy = encrypt_key_entry.get()
    if key_to_copy:
        pyperclip.copy(key_to_copy)

def encrypt_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            key = generate_key()
            key_label.config(text=f"Encryption Key: {key}")
            encrypt_key_entry.delete(0, tk.END)
            encrypt_key_entry.insert(0, key)
            
            with open(file_path, 'rb') as f:
                data = f.read()
            
            fernet = Fernet(key.encode())
            encrypted_data = fernet.encrypt(data)
            
            # Overwrite the original file with the encrypted data
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            messagebox.showinfo("Success", "File encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def decrypt_file():
    encrypted_file_path = filedialog.askopenfilename()
    if encrypted_file_path:
        try:
            key = simpledialog.askstring("Input", "Enter the decryption key:")
            if not key:
                messagebox.showerror("Error", "Please enter the decryption key.")
                return
            
            with open(encrypted_file_path, 'rb') as f:
                data = f.read()
            
            fernet = Fernet(key.encode())
            decrypted_data = fernet.decrypt(data)
            
            # Optionally, overwrite the encrypted file with the decrypted data
            with open(encrypted_file_path, 'wb') as f:
                f.write(decrypted_data)
            
            messagebox.showinfo("Success", "File decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("LockNKey")

    style = ttk.Style()
    style.configure("TButton", padding=5, font=("Segoe UI", 10))
    style.configure("TLabel", padding=5, font=("Segoe UI", 10))

    encrypt_button = ttk.Button(root, text="Encrypt File", command=encrypt_file)
    encrypt_button.pack(pady=10)

    key_frame = ttk.Frame(root)
    key_frame.pack(pady=5)

    key_label = ttk.Label(key_frame, text="Encryption Key:")
    key_label.grid(row=0, column=0, padx=5, pady=5)

    encrypt_key_entry = ttk.Entry(key_frame, width=50)

    copy_key_button = ttk.Button(key_frame, text="Copy Key", command=copy_key)
    copy_key_button.grid(row=0, column=2, padx=5, pady=5)

    decrypt_button = ttk.Button(root, text="Decrypt File", command=decrypt_file)
    decrypt_button.pack(pady=10)

    root.mainloop()
