import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Déclaration des comptes et transactions
accounts = {}
transactions = []

# Fonction pour ajouter un compte
def add_account():
    name = account_name_entry.get()
    initial_balance = initial_balance_entry.get()
    if name in accounts:
        messagebox.showerror("Erreur", f"Le compte '{name}' existe déjà.")
    else:
        try:
            balance = float(initial_balance)
            accounts[name] = balance
            messagebox.showinfo("Succès", f"Compte '{name}' ajouté avec un solde initial de {balance}.")
            account_name_entry.delete(0, tk.END)
            initial_balance_entry.delete(0, tk.END)
            update_account_list()
            update_account_combobox()
            update_pie_chart()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un solde initial valide.")

# Fonction pour ajouter une transaction
def add_transaction():
    account_name = trans_account_name_entry.get()
    type = trans_type_entry.get()
    amount = trans_amount_entry.get()
    if account_name in accounts:
        try:
            amount = float(amount)
            timestamp = datetime.now()  # Record current timestamp
            transactions.append((account_name, type, amount, timestamp))
            if type == 'revenu':
                accounts[account_name] += amount
            elif type == 'dépense':
                accounts[account_name] -= amount
            messagebox.showinfo("Succès", f"Transaction ajoutée : {type} de {amount} sur le compte '{account_name}'.")
            trans_account_name_entry.set('')
            trans_type_entry.set('')
            trans_amount_entry.delete(0, tk.END)
            update_account_list()
            update_pie_chart()
            plot_account_balance_over_time()  # Plot account balance over time
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
    else:
        messagebox.showerror("Erreur", f"Le compte '{account_name}' n'existe pas.")

# Fonction pour afficher le solde d'un compte
def get_balance():
    account_name = balance_account_name_entry.get()
    if account_name in accounts:
        balance = accounts[account_name]
        messagebox.showinfo("Solde du compte", f"Solde actuel du compte '{account_name}' : {balance}")
    else:
        messagebox.showerror("Erreur", f"Le compte '{account_name}' n'existe pas.")
    balance_account_name_entry.delete(0, tk.END)

# Mettre à jour la liste des comptes
def update_account_list():
    account_list.delete(*account_list.get_children())
    for account, balance in accounts.items():
        account_list.insert("", "end", values=(account, balance))

# Mettre à jour les noms des comptes dans la combobox des transactions
def update_account_combobox():
    trans_account_name_entry['values'] = list(accounts.keys())

# Fonction pour mettre à jour le graphique circulaire
def update_pie_chart():
    labels = accounts.keys()
    sizes = accounts.values()
    ax.clear()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#A15C33', '#0066CC', '#FFCC00', '#009966'])
    ax.axis('equal')
    canvas.draw()

# Fonction pour tracer l'évolution du solde du compte au fil du temps
def plot_account_balance_over_time():
    fig_balance_over_time.clf()  # Clear the previous plot
    for account in accounts:
        balance_over_time = []
        for transaction in transactions:
            if transaction[0] == account:  # Check if transaction is for the current account
                balance_over_time.append((transaction[3], accounts[account]))  # Append (timestamp, balance)
        balance_over_time.sort(key=lambda x: x[0])  # Sort by timestamp
        timestamps = [entry[0] for entry in balance_over_time]
        balances = [entry[1] for entry in balance_over_time]
        plt.plot(timestamps, balances, label=account)
    plt.xlabel('Time')
    plt.ylabel('Balance')
    plt.title('Evolution des comptes au fil du temps')
    plt.legend()
    fig_balance_over_time.autofmt_xdate()  # Rotate x-axis labels for better readability
    canvas_balance_over_time.draw()

# Interface graphique
def main():
    global account_name_entry, initial_balance_entry, trans_account_name_entry, trans_type_entry, trans_amount_entry, balance_account_name_entry, account_list, canvas, ax, fig_balance_over_time, canvas_balance_over_time

    root = tk.Tk()
    root.title("Gestion de Compte Bancaire")
    root.geometry("1024x768")
    root.configure(bg='#2E2E2E')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TLabel", font=("Helvetica", 12), background='#2E2E2E', foreground='#FFFFFF')
    style.configure("TButton", font=("Helvetica", 12), background='#4CAF50', foreground='#FFFFFF')
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("Treeview", font=("Helvetica", 10), background='#EFEFEF', foreground='#000000', fieldbackground='#EFEFEF')
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background='#007BFF', foreground='#FFFFFF')
    style.map("TButton", background=[('active', '#45a049')])

    # Cadre pour ajouter un compte
    frame_add_account = tk.LabelFrame(root, text="Ajouter un Compte", bg='#2E2E2E', fg='#FFFFFF', bd=5, relief=tk.RIDGE)
    frame_add_account.pack(pady=10, padx=10, fill=tk.X)

    tk.Label(frame_add_account, text="Nom du compte:", bg='#2E2E2E', fg='#FFFFFF').grid(row=0, column=0, pady=5, padx=5)
    account_name_entry = ttk.Entry(frame_add_account)
    account_name_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(frame_add_account, text="Solde initial:", bg='#2E2E2E', fg='#FFFFFF').grid(row=1, column=0, pady=5, padx=5)
    initial_balance_entry = ttk.Entry(frame_add_account)
    initial_balance_entry.grid(row=1, column=1, pady=5, padx=5)

    ttk.Button(frame_add_account, text="Ajouter un compte", command=add_account).grid(row=2, columnspan=2, pady=10)

    # Cadre pour ajouter une transaction
    frame_add_transaction = tk.LabelFrame(root, text="Ajouter une Transaction", bg='#2E2E2E', fg='#FFFFFF
