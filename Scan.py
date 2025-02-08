import socket
from tkinter import *
from tkinter import ttk,END
import tkinter as tk
from tkinter import simpledialog

#Finir l'interface (voir croquis) et après mettre des animations (de chargement, sur les boutons etc...)

root = Tk()
root.title("Scanner de ports")
root.geometry("100x100")
entry = ttk.Entry(root) #Pour mettre un input
entry.pack()

text_area = Text(root,height=20,width=150)
text_area.pack()

valeur = StringVar()
valeur.set("")
entree = Entry(root,textvariable=valeur,width=30)
entree.pack()


label = Label(root, text="Entrée utilisateur")
label.pack()

#Entrée utilisateurs 

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
            text_area.insert(f"port {port} : Ouvert.")
            ports_ouvert.append(port)  
        sock.close()
    if ports_ouvert:
        ports_ouvert = ", ".join(map(str, ports_ouvert))  # Transforme la liste en texte
        text_area.insert(END,f"Ports ouvert sur une plage de {ports} : {ports_ouvert}")
    else:
        text_area.insert(END,f"Aucun port ouvert détecté sur l'adresse : {adresse}")


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
        text_area.insert(END,f"\n Port {port} : Ouvert")
    else:
        text_area.insert(END,f"\n Port {port} : Fermé")
    sock.close()
    

bouton = Button(root,text="Scanner un port spécifique", command=lancer_scan_port)
bouton.place(x=10,y=200)  
bouton = Button(root,text="Scanner une plage de ports", command=lancer_scan_plage)
bouton.place(x=10,y=240)  


root.mainloop()
#if __name__ == '__main__':
 #   main()