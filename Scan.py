import socket

#Entrée utilisateurs 

def choix():
    choix_domaine_ip = int(input("Voulez vous scanner : 1) Une adresse IP (par exemple : 127.0.0.1) \n 2) Un domaine ? (exemple.com) \n 3) Quitter\n "))

    if choix_domaine_ip == 1:
        ip = input("Entrez l'adresse ip souhaiter : ")
        return ip
    elif choix_domaine_ip == 2:
        domaine = input("Entrez le nom de domaine souhaiter (dans le format : exemple.com) : ")
        return domaine
    elif choix_domaine_ip == 3:
        print("Au revoir...")
        exit()
    else:
        print("Choix invalide, veuillez entrer un choix entre 1 et 2.")    
        return choix()
        
print("Des exemples de ports : 80 (HTTP), 443 (HTTPS), 22 (SSH) etc...")

def main():
    
    
    choix_methode = int(input("1) Scanner un port en particulier \n 2) Scanner une plage de ports \n : "))
    adresse = choix()
    if choix_methode == 1:
        port = int(input("Entrez le port à scanner : "))
        print(test_single_port(adresse,port))
    if choix_methode == 2:
        ports = int(input("Entrer la plage de ports à scanner (de 1 à 1024): "))
        while True:
            if ports > 1024:
                print("Plage invalide, veuillez entrer une plage entre 1 et 1024")
            else:
                print("Veuillez entrer un choix valide.")
                break
        print(f"Scanning adress : {adresse}")
        print(verification_ports(ports, adresse))
        


def verification_ports(ports,adresse):
    ports_ouvert = []
    for port in range(1, ports+1):
        print(f"Scan du port {port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((adresse,port))
        if result == 0:
            print(f"port {port} : Ouvert.")
            ports_ouvert.append(port)
            
        sock.close()
    return f"Ports ouvert sur une plage de {ports} : {ports_ouvert}"


def test_single_port(adresse, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((adresse, port))
    if result == 0:
        print(f"Port {port} : Ouvert")
    else:
        print(f"Port {port} : Fermé")
    sock.close()
    


if __name__ == '__main__':
    main()