# Import modules
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pyperclip
from cryptography.fernet import Fernet
import tkinter.ttk as ttk

# Generate encryption key
def generate_key():
    # Generate and Decode base64 key
    return Fernet.generate_key().decode()

# Copy the encryption key to the clipboard
def copy_key():
    key_to_copy = encrypt_key_entry.get()
    if key_to_copy:
        pyperclip.copy(key_to_copy)

# Encrypt a file
def encrypt_file():
    # Open file explorer to get file to encrypt
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # Generate key and update the GUI to show the key
            key = generate_key()
            key_label.config(text=f"Encryption Key: {key}")
            encrypt_key_entry.delete(0, tk.END)
            encrypt_key_entry.insert(0, key)
            
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encrypt data
            fernet = Fernet(key.encode())
            encrypted_data = fernet.encrypt(data)
            
            # Overwrite file with encrypted data
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Display success message
            messagebox.showinfo("Success", "File encrypted successfully!")
        except Exception as e:
            # Display error message if catch
            messagebox.showerror("Error", f"An error occurred: {e}")

# Decrypt a file
def decrypt_file():
    # Open file explorer to get encrypted file
    encrypted_file_path = filedialog.askopenfilename()
    if encrypted_file_path:
        try:
            # Prompt to get key
            key = simpledialog.askstring("Input", "Enter the decryption key:")
            if not key:
                messagebox.showerror("Error", "Please enter the decryption key.")
                return
            
            # Read encrypted file
            with open(encrypted_file_path, 'rb') as f:
                data = f.read()
            
            # Decrypt data using key
            fernet = Fernet(key.encode())
            decrypted_data = fernet.decrypt(data)
            
            # Overwrite encrypted file with decrypted data
            with open(encrypted_file_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Display success message
            messagebox.showinfo("Success", "File decrypted successfully!")
        except Exception as e:
            # Display error message if catch
            messagebox.showerror("Error", f"An error occurred: {e}")

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("LockNKey")

    # Font and Style
    style = ttk.Style()
    style.configure("TButton", padding=5, font=("Segoe UI", 10))
    style.configure("TLabel", padding=5, font=("Segoe UI", 10))

    # Encrypt button
    encrypt_button = ttk.Button(root, text="Encrypt File", command=encrypt_file)
    encrypt_button.pack(pady=10)

    # Frame
    key_frame = ttk.Frame(root)
    key_frame.pack(pady=5)

    # Display for encryption key
    key_label = ttk.Label(key_frame, text="Encryption Key:")
    key_label.grid(row=0, column=0, padx=5, pady=5)
    encrypt_key_entry = ttk.Entry(key_frame, width=50)

    # Copy key button
    copy_key_button = ttk.Button(key_frame, text="Copy Key", command=copy_key)
    copy_key_button.grid(row=0, column=2, padx=5, pady=5)

    # Decrypt button
    decrypt_button = ttk.Button(root, text="Decrypt File", command=decrypt_file)
    decrypt_button.pack(pady=10)

    root.mainloop()
