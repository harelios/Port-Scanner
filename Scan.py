import socket
from tkinter import *
from tkinter import ttk,END
import tkinter as tk
from tkinter import simpledialog


root = Tk()
root.title("Scanner de ports")
root.geometry("100x100")

text_area = Text(root,height=20,width=150)
text_area.pack()

valeur = StringVar()
valeur.set("")

root.configure(bg = "#23272A") #couleur de fond gris foncé
text_area.configure(bg = "#23272A", fg="white", font=("consolas", 12)) # Zone de texte en mode terminal

style = ttk.Style()
style.configure("Hover.TButton",font=("Arial",12,"bold") , foreground="black", background="#5865F2", padding="10")




def on_enter(e):
    e.widget.configure(style="Hover.TButton")
    

def on_leave(e):
    e.widget.configure(style="TButton") 

def choix():
    text_area.insert(END,"Voulez vous scanner : 1) Une adresse IP (par exemple : 127.0.0.1) \n 2) Un domaine ? (exemple.com) \n 3) Quitter\n ")
    choix_domaine_ip = int(recupere())
    
    if choix_domaine_ip == 1:
        text_area.insert(END,"Entrez l'adresse ip souhaiter : ")
        recupere()
    elif choix_domaine_ip == 2:
        text_area.insert(END,"Entrez le nom de domaine souhaiter (dans le format : exemple.com) : ")
        recupere()
    elif choix_domaine_ip == 3:
        text_area.insert("Au revoir...")
        exit()
    else:
        text_area.insert("Choix invalide, veuillez entrer un choix entre 1 et 2.")    
        choix()
        
text_area.insert(END,"Des exemples de ports : 80 (HTTP), 443 (HTTPS), 22 (SSH) etc...")    
    
    
def recupere():
    return valeur.get()

def verification_ports(ports,adresse):
    ports_ouvert = []
    for port in range(1, ports+1):
        text_area.insert(END,f"Scan du port {port}...\n")
        text_area.update_idletasks()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((adresse,port))
        if result == 0:
            text_area.insert(END,f"port {port} : Ouvert.\n")
            ports_ouvert.append(port)  
        sock.close()
        if port > ports+1:
            break
    if ports_ouvert:
        ports_ouvert = ", ".join(map(str, ports_ouvert))  # Transforme la liste en texte
        text_area.insert(END,f"Ports ouvert sur une plage de {ports} : port(s) {ports_ouvert}")
    else:
        text_area.insert(END,f"Aucun port ouvert détecté sur l'adresse : {adresse} \n")
        


def lancer_scan_port():
    adresse = simpledialog.askstring("Adresse","Entrez l'adresse ip ou le domaine à scanner : ")
    port = simpledialog.askstring("Port","Entrer un port à scanner : ")
    port = int(port)
    
    if not adresse:
        text_area.insert(END,"Aucune adresse saisie, veuillez entrer une adresse valide.")
        return
    elif not port:
        text_area.insert(END,"Aucun port entrer, veuillez entrer un port valide.")
        return
    text_area.insert(END, f"\n Scan en cours sur {adresse}, port {port}...\n")
    test_single_port(adresse,port)
    
def lancer_scan_plage():
    adresse = simpledialog.askstring("Entrée utilisateur","Entrer l'adresse ou le domaine à scanner : ")
    ports = simpledialog.askstring("Entrée utilisateur","Entrer la plage de ports à scanner (entre 1 à 1024) : ")
    
    if not adresse:
        text_area.insert(END,"Aucune adresse saisie, veuillez entrer une adresse valide.")
        return
    elif not ports.isdigit():
        text_area.insert(END,"Aucun port entrer, veuillez entrer un port valide. (1-1024).")
        return
    ports = int(ports)
    if ports >1024:
        text_area.insert(END,"Veuillez entrer une plage de port entre 1 et 1024.") 
        return
    text_area.insert(END, f"Scan des ports 1 à {ports} sur {adresse}...\n")
    verification_ports(int(ports), adresse)
    
def test_single_port(adresse, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((adresse, port))
    if result == 0:
        text_area.insert(END,f"\n Port {port} : Ouvert \n")
    else:
        text_area.insert(END,f"\n Port {port} : Fermé \n")
    sock.close()
    
bouton_single_port = ttk.Button(root,text="Scanner un port spécifique", command=lancer_scan_port, style="TButton")
bouton_single_port.bind("<Enter>",on_enter)
bouton_single_port.bind("<Leave>", on_leave)
bouton_single_port.place(x=600,y=400)  

bouton_plage_port = ttk.Button(root,text="Scanner une plage de ports", command=lancer_scan_plage, style="TButton")
bouton_plage_port.bind("<Enter>",on_enter)
bouton_plage_port.bind("<Leave>", on_leave)
bouton_plage_port.place(x=600,y=450)  

bouton_quit = ttk.Button(root,text="Quitter", command=root.quit)
bouton_quit.bind("<Enter>",on_enter)
bouton_quit.bind("<Leave>", on_leave)
bouton_quit.place(x=600,y=500)
root.mainloop()