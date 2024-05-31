import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# Données globales
comptes = {}
transactions = []
transactions_recurrentes = []
date_actuelle = datetime.now()


def ajouter_compte():
    nom_compte = entree_nom_compte.get()
    solde_initial = entree_solde_initial.get()
   
    if nom_compte and solde_initial:
        try:
            solde_initial = float(solde_initial)
            comptes[nom_compte] = solde_initial
            entree_nom_compte.delete(0, tk.END)
            entree_solde_initial.delete(0, tk.END)
            mettre_a_jour_liste_comptes()
            mettre_a_jour_combobox_comptes()
            mettre_a_jour_camembert()
            tracer_solde_comptes_dans_temps()
        except ValueError:
            messagebox.showerror("Erreur", "Le solde initial doit être un nombre.")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

        

def ajouter_transaction():
    nom_compte = entree_nom_compte
    type_trans = entree_type_trans.get()
    montant = entree_montant_trans.get()
   
    if nom_compte and type_trans and montant:
        try:
            montant = float(montant)
            if type_trans == "dépense":
                montant = -montant
            comptes[nom_compte] += montant
            transactions.append((date_actuelle, nom_compte, montant))
            entree_montant_trans.delete(0, tk.END)
            mettre_a_jour_liste_comptes()
            mettre_a_jour_camembert()
            tracer_solde_comptes_dans_temps()
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre.")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        

def ajouter_trans_recurrente():
    nom_compte = entree_nom_compte_trans_rec.get()
    type_trans = entree_type_trans_rec.get()
    montant = entree_montant_trans_rec.get()
    frequence = entree_frequence_trans_rec.get()
   
    if nom_compte and type_trans and montant and frequence:
        try:
            montant = float(montant)
            frequence = int(frequence)
            if type_trans == "dépense":
                montant = -montant
            transactions_recurrentes.append((nom_compte, montant, frequence))
            entree_montant_trans_rec.delete(0, tk.END)
            entree_frequence_trans_rec.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erreur", "Le montant et la fréquence doivent être des nombres.")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

def mettre_a_jour_date_actuelle():
    global date_actuelle
    nouvelle_date = entree_date_actuelle.get()
    try:
        nouvelle_date_obj = datetime.strptime(nouvelle_date, '%Y-%m-%d')
        if nouvelle_date_obj > date_actuelle:
            date_actuelle = nouvelle_date_obj
            etiquette_date_actuelle.config(text=f"Date actuelle: {date_actuelle.strftime('%Y-%m-%d')}")
            traiter_transactions_recurrentes()
            mettre_a_jour_liste_comptes()
            mettre_a_jour_camembert()
            tracer_solde_comptes_dans_temps()
        else:
            messagebox.showerror("Erreur", "La nouvelle date doit être postérieure à la date actuelle.")
    except ValueError:
        messagebox.showerror("Erreur", "La date doit être au format AAAA-MM-JJ.")

def traiter_transactions_recurrentes():
    global transactions_recurrentes, transactions, comptes
    for trans_rec in transactions_recurrentes:
        nom_compte, montant, frequence = trans_rec
        derniere_date = max([trans[0] for trans in transactions if trans[1] == nom_compte], default=date_actuelle - timedelta(days=frequence))
        jours_depuis_derniere = (date_actuelle - derniere_date).days
        occurrences = jours_depuis_derniere // frequence
       
        for i in range(occurrences):
            date_trans = derniere_date + timedelta(days=frequence*(i+1))
            transactions.append((date_trans, nom_compte, montant))
            comptes[nom_compte] += montant

def mettre_a_jour_liste_comptes():
    for i in liste_comptes.get_children():
        liste_comptes.delete(i)
    for compte, solde in comptes.items():
        liste_comptes.insert('', tk.END, values=(compte, f"{solde:.2f}"))

def mettre_a_jour_combobox_comptes():
    noms_comptes = list(comptes.keys())
    entree_nom_compte_trans['values'] = noms_comptes
    entree_nom_compte_trans_rec['values'] = noms_comptes

def mettre_a_jour_camembert():
    ax.clear()
    noms_comptes = list(comptes.keys())
    soldes = [comptes[compte] for compte in noms_comptes]
    ax.pie(soldes, labels=noms_comptes, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(soldes))))
    ax.set_title("Répartition des soldes des comptes", color="#ffffff")
    canvas.draw()

def tracer_solde_comptes_dans_temps():
    ax_solde_dans_temps.clear()
    noms_comptes = list(comptes.keys())
    for compte in noms_comptes:
        dates = [trans[0] for trans in transactions if trans[1] == compte]
        montants = [trans[2] for trans in transactions if trans[1] == compte]
        soldes = [sum(montants[:i+1]) for i in range(len(montants))]
        ax_solde_dans_temps.plot(dates, soldes, label=compte)
    ax_solde_dans_temps.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax_solde_dans_temps.set_title("Évolution du solde des comptes dans le temps", color="#ffffff")
    ax_solde_dans_temps.legend()
    ax_solde_dans_temps.tick_params(colors='#ffffff')
    canvas_solde_dans_temps.draw()

def main():
    global entree_nom_compte, entree_solde_initial, entree_nom_compte_trans, entree_type_trans, entree_montant_trans
    global entree_nom_compte_trans_rec, entree_type_trans_rec, entree_montant_trans_rec, entree_frequence_trans_rec
    global entree_date_actuelle, etiquette_date_actuelle, liste_comptes, fig, ax, canvas, fig_solde_dans_temps, ax_solde_dans_temps, canvas_solde_dans_temps

    root = tk.Tk()
    root.title("Gestion de Compte Bancaire")
   
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#2c2f33")
    style.configure("TLabel", background="#2c2f33", foreground="#ffffff", font=("Arial", 12))
    style.configure("TButton", background="#7289da", foreground="#ffffff", font=("Arial", 12, "bold"))
    style.configure("TEntry", fieldbackground="#23272a", foreground="#ffffff", font=("Arial", 12))
    style.configure("TCombobox", fieldbackground="#23272a", foreground="#ffffff", font=("Arial", 12))
    style.configure("TLabelframe", background="#2c2f33", foreground="#ffffff", font=("Arial", 14, "bold"))
    style.configure("TLabelframe.Label", background="#2c2f33", foreground="#ffffff", font=("Arial", 14, "bold"))

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
   
    canvas_principal = tk.Canvas(main_frame, bg="#2c2f33")
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas_principal.yview)
    frame_defilement = ttk.Frame(canvas_principal)
   
    frame_defilement.bind(
        "<Configure>",
        lambda e: canvas_principal.configure(
            scrollregion=canvas_principal.bbox("all")
        )
    )

    canvas_principal.create_window((0, 0), window=frame_defilement, anchor="nw")
    canvas_principal.configure(yscrollcommand=scrollbar.set)

    canvas_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Ajouter un compte
    frame_ajouter_compte = ttk.Labelframe(frame_defilement, text="Ajouter un compte", padding=(20, 10))
    frame_ajouter_compte.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W+tk.E)

    ttk.Label(frame_ajouter_compte, text="Nom du compte:").grid(row=0, column=0, padx=5, pady=5)
    entree_nom_compte = ttk.Entry(frame_ajouter_compte)
    entree_nom_compte.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_ajouter_compte, text="Solde initial:").grid(row=1, column=0, padx=5, pady=5)
    entree_solde_initial = ttk.Entry(frame_ajouter_compte)
    entree_solde_initial.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(frame_ajouter_compte, text="Ajouter", command=ajouter_compte).grid(row=2, column=0, columnspan=2, pady=10)

    # Ajouter une transaction
    frame_ajouter_transaction = ttk.Labelframe(frame_defilement, text="Ajouter une transaction", padding=(20, 10))
    frame_ajouter_transaction.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W+tk.E)

    ttk.Label(frame_ajouter_transaction, text="Nom du compte:").grid(row=0, column=0, padx=5, pady=5)
    entree_nom_compte_trans = ttk.Combobox(frame_ajouter_transaction, state="readonly")
    entree_nom_compte_trans.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_ajouter_transaction, text="Type:").grid(row=1, column=0, padx=5, pady=5)
    entree_type_trans = ttk.Combobox(frame_ajouter_transaction, values=["revenu", "dépense"], state="readonly")
    entree_type_trans.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_ajouter_transaction, text="Montant:").grid(row=2, column=0, padx=5, pady=5)
    entree_montant_trans = ttk.Entry(frame_ajouter_transaction)
    entree_montant_trans.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(frame_ajouter_transaction, text="Ajouter", command=ajouter_transaction).grid(row=3, column=0, columnspan=2, pady=10)

    # Ajouter une transaction récurrente
    frame_ajouter_transaction_rec = ttk.Labelframe(frame_defilement, text="Ajouter une transaction récurrente", padding=(20, 10))
    frame_ajouter_transaction_rec.grid(row=2, column=0, padx=20, pady=20, sticky=tk.W+tk.E)

    ttk.Label(frame_ajouter_transaction_rec, text="Nom du compte:").grid(row=0, column=0, padx=5, pady=5)
    entree_nom_compte_trans_rec = ttk.Combobox(frame_ajouter_transaction_rec, state="readonly")
    entree_nom_compte_trans_rec.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_ajouter_transaction_rec, text="Type:").grid(row=1, column=0, padx=5, pady=5)
    entree_type_trans_rec = ttk.Combobox(frame_ajouter_transaction_rec, values=["revenu", "dépense"], state="readonly")
    entree_type_trans_rec.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_ajouter_transaction_rec, text="Montant:").grid(row=2, column=0, padx=5, pady=5)
    entree_montant_trans_rec = ttk.Entry(frame_ajouter_transaction_rec)
    entree_montant_trans_rec.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_ajouter_transaction_rec, text="Fréquence (jours):").grid(row=3, column=0, padx=5, pady=5)
    entree_frequence_trans_rec = ttk.Entry(frame_ajouter_transaction_rec)
    entree_frequence_trans_rec.grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(frame_ajouter_transaction_rec, text="Ajouter", command=ajouter_trans_recurrente).grid(row=4, column=0, columnspan=2, pady=10)

    # Mettre à jour la date actuelle
    frame_mettre_a_jour_date = ttk.Labelframe(frame_defilement, text="Mettre à jour la date actuelle", padding=(20, 10))
    frame_mettre_a_jour_date.grid(row=3, column=0, padx=20, pady=20, sticky=tk.W+tk.E)

    ttk.Label(frame_mettre_a_jour_date, text="Nouvelle date (AAAA-MM-JJ):").grid(row=0, column=0, padx=5, pady=5)
    entree_date_actuelle = ttk.Entry(frame_mettre_a_jour_date)
    entree_date_actuelle.grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(frame_mettre_a_jour_date, text="Mettre à jour", command=mettre_a_jour_date_actuelle).grid(row=1, column=0, columnspan=2, pady=10)
    etiquette_date_actuelle = ttk.Label(frame_mettre_a_jour_date, text=f"Date actuelle: {date_actuelle.strftime('%Y-%m-%d')}")
    etiquette_date_actuelle.grid(row=2, column=0, columnspan=2, pady=5)

    # Liste des comptes
    frame_liste_comptes = ttk.Labelframe(frame_defilement, text="Liste des comptes", padding=(20, 10))
    frame_liste_comptes.grid(row=4, column=0, padx=20, pady=20, sticky=tk.W+tk.E)

    colonnes = ('compte', 'solde')
    liste_comptes = ttk.Treeview(frame_liste_comptes, columns=colonnes, show='headings', height=8)
    liste_comptes.heading('compte', text='Nom du compte')
    liste_comptes.heading('solde', text='Solde')
    liste_comptes.column('compte', anchor=tk.CENTER)
    liste_comptes.column('solde', anchor=tk.CENTER)
    liste_comptes.tag_configure('evenrow', background='#3e4147')
    liste_comptes.tag_configure('oddrow', background='#2c2f33')
   
    liste_comptes.pack(fill=tk.BOTH, expand=True)

    # Graphiques
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(aspect="equal"))
    fig.patch.set_facecolor('#2c2f33')
    ax.set_facecolor('#2c2f33')
    canvas = FigureCanvasTkAgg(fig, master=frame_defilement)
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=4, padx=20, pady=20)

    fig_solde_dans_temps, ax_solde_dans_temps = plt.subplots(figsize=(8, 4))
    fig_solde_dans_temps.patch.set_facecolor('#2c2f33')
    ax_solde_dans_temps.set_facecolor('#2c2f33')
    canvas_solde_dans_temps = FigureCanvasTkAgg(fig_solde_dans_temps, master=frame_defilement)
    canvas_solde_dans_temps.get_tk_widget().grid(row=4, column=1, padx=20, pady=20)

    mettre_a_jour_liste_comptes()
    mettre_a_jour_combobox_comptes()
    mettre_a_jour_camembert()
    tracer_solde_comptes_dans_temps()

    root.mainloop()

if __name__ == "__main__":
    main()
