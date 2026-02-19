# DEPENDANCES
# Installation du package Requests pour requêter en HTTP : Python -m pip install requests
# Installation du package BeautifullSoup pour parser du HTML : Python -m pip install beautifulsoup4
# Documentation Beautifull Soup : https://www.crummy.com/software/BeautifulSoup/
# Installation du package Newspaper3k pour identifier les articles sur des sites d'information : Python -m pip install newspaper3k
# Documentation : https://scrapeops.io/python-web-scraping-playbook/newspaper3k/ et https://pypi.org/project/newspaper3k/ 

# FICHIERS
# Pour la saisie des mots clés et sites les fichiers utilisés pour stocker les données saisies sont : 
# liste_mots.txt  : stocke la liste des mots clés saisis à la dernière utilisation pour pouvoir la recharger à l'utilisation suivante
# liste_sites.txt : stocke la liste des sites saisis à la dernière utilisation pour pouvoir la recharger à l'utilisation suivante

# VARIABLES 1/2
# Pour la saisie des mots clés et sites les variables utilisées sont :
# saisie : stocke temporairerement les saisies de sites et mots clés (en input puis en affichage)
# motscle: liste des mots clés saisis
# nb_mots_clés : comme son nom l'indique
# sites : liste des sites à surveiller
# nb_sites : comme son nom l'indique

# VARIABLES 2/2
# Pour la construction du dictionnaire contenant tous les articles d'une page, les variables utilisées sont :
# resultat : réponse HTTP du site web scrappé
# soup : code html transformé en chaine de caractères
# article_list : la liste des tous les articles d'une page
# article_tag : un article de la liste en particulier sur lequel on va récupérer les infos ci-dessous
# dico_articles : dictionnaire avec l'url d'un article en clé (chaine de caractères site) et le dictionnaire dico_metadonnees en valeur
# dico_metadonnees : dictionnaire avec toutes les métadonnées relatives à un article : titre, résumé, date, liste des mots clés détectés
# Cette structure correspond à une BdD SQL avec une table principale liste_articles et une table secondaire site_infos dont site est la clé étrangère et qui contient toutes les métadonnées de chaque site
# article_tag_url : url
# article_tag_title : titre
# article_tag_sumup : résumé
# article_tag_date : date
# article_tag_keywords : liste des mots clés

import requests
from bs4 import BeautifulSoup

# Saisie de la liste de mots clés à rechercher - on les enregistre dans un fichier liste_mots pour recharge à prochaine utilisation si besoin
print("\n\nVous allez maintenant saisir les mots clés sur lesquels vous souhaitez orienter votre veille")
print("Chaque mot-clé est une chaine de caractères indépendante")
print("Le logiciel recherchera l'un des mots clés demandés dans les articles en ligne")
print("Les mots clés ne différencient pas les minuscules des majuscules")
print("Si vous saisissez plusieurs mots clés à la suite comme 'revue hebdomadaire' alors c'est la chaine complète de caractères qui sera recherchée et non un mot ou l'autre")
print("Lorsque vous avez fini de saisir les mots clés recherchés tapez juste #STOP# pour arrêter... N'oubliez pas les majucules et les #")
print("Si vous voulez recharger votre précédente liste de mots clés tapez juste #CHARGER#.. N'oubliez pas les majucules et les #")
print("A vous de jouer...\n\n")
saisie = ""
motscle =[]
nb_mots_clés = 1
saisie = input("Saisissez le mots clé n°"+str(nb_mots_clés)+"\n")
if saisie == "#CHARGER#": #Charge la liste des mots clés saisis au dernier lancement du programme
    file = open("liste_mots.txt", "r", encoding="utf-8")
    motscle = file.read().splitlines() #On lit le fichier et on crée une liste dont chaque éléments est séparé par un retour à la ligne dans le fichier texte
    nb_mots_clés = len(motscle)+1
else: #Fait saisir les mots clés et les enregistre dans un fichier pour une prochaine utilisation du programme
    file = open("liste_mots.txt", "w", encoding="utf-8")
    while saisie != "#STOP#":
        file.write(saisie+"\n")
        motscle.append(saisie)   
        nb_mots_clés = len(motscle)+1
        saisie = input("Saisissez le mots clé n°"+str(nb_mots_clés)+"\n")
file.close()           

# Saisie de l'URL à scrapper - on les enregistre dans un fichier liste_sites pour recharge à prochaine utilisation si besoin
print("\n\nVous allez maintenant saisir les sites web sur lesquels vous souhaitez orienter votre veille")
print("Saississez un seul site web à la fois")
print("N'oubliez pas de saisir le protocle lié au site web qui commence généralement par 'https://www'")
print("Le logiciel recherchera chaque mot clé demandé dans tous les sites web indiqués")
print("Lorsque vous avez fini de saisir les sites web recherchés tapez juste #STOP# pour arrêter... N'oubliez pas les majucules et les #")
print("Si vous voulez recharger votre précédente liste de sites tapez juste #CHARGER#.. N'oubliez pas les majucules et les #")
print("A vous de jouer...\n\n\n")
saisie = ""
sites =[]
nb_sites = 1
saisie = input("Saisissez l'adresse du site web n°"+str(nb_sites)+" à surveiller\n")
if saisie == "#CHARGER#": #Charge la liste des sites saisis au dernier lancement du programme
    file = open("liste_sites.txt", "r", encoding="utf-8")
    sites = file.read().splitlines() #On lit le fichier et on crée une liste dont chaque éléments est séparé par un retour à la ligne dans le fichier texte
    nb_sites = len(sites)+1
else: #Fait saisir les mots clés et les enregistre dans un fichier pour une prochaine utilisation du programme
    file = open("liste_sites.txt", "w", encoding="utf-8")
    while saisie != "#STOP#":
        try:
            if "200" in str(requests.get(saisie)) :
                file.write(saisie+"\n")
                sites.append(saisie)
                nb_sites = len(sites)+1
                saisie = input("Saisissez l'adresse du site web n°"+str(nb_sites)+" à surveiller\n")
            elif saisie != "#STOP#": #Le paragraphe elif vise à traiter le cas où le site web ne répond pas correctement
                print("Le site web que vous avez mentionné ne semble pas répondre correctement")
                print("Le code HTTP renvoyé est",str(requests.get(saisie)))
        except: #Le paragraphe except vise à traiter le cas où l'adresse web saisie n'est pas correcte
            print("L'adresse du site web saisie n'est pas correcte")
            print("Avez-vous pensé à mentionner le protocole type 'http://wwww.' ?\n")
# Récapitulatif
print("\nVous avez décidé de rechercher les mots clés suivants :")
for saisie in motscle:
    print("- ",saisie)
print("\nCes mots clés seront recherchés dans les sites suivants")
for saisie in sites:
    print("- ",saisie)
print("\n")

#Inititiation du dictionnaire de mes résultats de scrapping
dico_articles = {}

for saisie in sites: #On parcourt la liste des url saisies par l'opérateur pour les scrapper
    # Attention, pour le moment, les balises utilisées pour la recherche de données sur la page correspondent à l'url ci-dessous (à généraliser) :
    # 'https://www.navalnews.com/category/naval-news/'

    resultat = requests.get(saisie) #On récupère la réponse http du site web mais on ne peut pas l'interpréter
    soup = BeautifulSoup(resultat.content,"html.parser") #On transforme le code html en chaine de caractères avec le parser html.parser inclus dans Python (sinon il faut installer une dépendance dédiée)
    article_list = soup.select('article') #On crée la liste de toutes les balises "article" du site

    for article_tag in article_list:
        #Inititiation du dictionnaire de métadonnées vierge
        dico_metadonnees = {'titre': "x", 'résumé': "x", 'date': "x", 'texte': "x", 'mots clés': []}
        # Extraction des métadonnées
        article_tag_url = article_tag.find('a').get('href') #On récupère le lien de l'article après la balise <a dans l'id href
        article_tag_title = article_tag.find('h3').get_text().strip() #On récupère le titre de l'article après la balise h3 et le strip retire les espaces vides de début et fin
        article_tag_sumup = article_tag.find('p').get_text().strip() #On récupère le résumé de l'article après la balise p
        article_tag_date = article_tag.find('span').get_text().strip() #On récupère la date de l'article après la balise span
        #Recherche des mots-clés
        for mot in motscle:
            if mot.lower() in str(soup).lower():
                #Si le mot clé est présent dans le code hltm, on l'ajoute aux mots-clés trouvés
                #Tout est passé en lower case pour ne pas être sensible à la casse
                dico_metadonnees["mots clés"].append(mot)
            if mot.lower() in str(soup).lower() and dico_metadonnees["titre"]=="x":
                #Si c'est le premier mot clé trouvé sur cet article, on ajoute les métadonnées communes à tout l'article
                dico_metadonnees["titre"]=article_tag_title
                dico_metadonnees["résumé"]=article_tag_sumup
                dico_metadonnees["date"]=article_tag_date
        #Si on a trouvé au moins un mot clé dans l'article alors on le référence dans notre dico de résultats
        if len(dico_metadonnees["mots clés"]) > 0:
            dico_articles[article_tag_url]=dico_metadonnees
            print("Sur le site", article_tag_url, "nous avons trouvé :")
            print("- les mots clés suivants :", dico_metadonnees["mots clés"])
            print("- le titre de l'article est :", article_tag_title)
            print("- le résumé de l'article est :", article_tag_sumup)
            print("- la date de l'article est :", article_tag_date)
            print("\n")
    
if dico_articles == {}:
    print("Nous n'avons pas trouvé vos mots clés dans les sites scrappés")
    print("\n")


    


    # J'en suis là : 
    # J'ai à jour mon big dico d'articles pour tous les articles du site de la première boucle (qui ne marche pour le moment que pour un site)
    # Faut maintenant que je vérifie si ça itère pour tous les sites 'saisie' de la liste 'sites'.
    # Tester avec https://www.naval-group.com/fr et https://www.navalnews.com/category/naval-news/
    # J'ai l'impression qu'il faut que je trouve toutes les balises <a puis que je remonte au-dessus d'elles pour trouver titre, résumé et date... 
    # Mais pas sûr qu'on ait ces infos sur tous les sites donc il faudra peut être que j'explore l'URL associée à la balise <a à la recherche des mots clés et autres infos
    # Ensuite j'afficherai les résultats de la recherche via mon big dico et une boucle FOR dédiée


        