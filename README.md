# MBE Preprocessing Interfaces

## Description

Ce projet consiste à transformer les données MBE venant de divers formats (.tdms, .log, .csv) en une base de données SQL exploitable pour une IA. Le PDF du rapport peut être trouvé à la racine de ce projet.

## Utilisation

Pour lancer le projet, il suffit de lancer `docker-compose up` et de naviguer vers `http://127.0.0.1:8000` puis cliquer sur `Ajouter une expérience`.

## Ce qu'il reste à faire

Il reste des détails à régler ainsi que des gros problèmes à résoudre.

Détails :

* Il faut ajouter le groupe d'expérience et le label comme arguments à la requête vers l'orchestrator de sorte à ce que celui-ci puisse les envoyer vers le container de temps absolu qui va ensuite les entrer dans la base. Actuellement, le label et le groupe d'expérience ne sont pas présents dans la BDD.

* Il faut que l'interface Django refuse d'ajouter une nouvelle expérience tant que l'expérience précédente est encore en cours (ou que l'orchestrator s'en charge, tant que l'utilisateur sait que l'ajout a été refusé).

* Il faut que l'orchestrator et le container des capteurs (celui qui est le plus lent, très largement) envoient des mise à jour du progrès du traitement des données. Traiter les données de réflectivité peut prendre des heures.

* Le container de temps absolu se comporte bien mais il faudrait ajouter la même gestion des erreurs au container de temps relatif et au container des capteurs.

Problèmes :

* Les fichiers "Wafer Temperature.tdms" ne peuvent pas être ouverts en utilisant npTDMS (la seule librairie Python que j'ai trouvé pour ouvrir un fichier TDMS) car ces fichiers utilisent le type `ExtendedFloat`. Soit il faut modifier le code source pour forcer un autre type sans que les données deviennent fausses, soit il faut trouver une autre librairie, soit il faut changer de langage.

## Perspective

Il reste comme piste d’amélioration majeur le fait que l’interface idéale est une interface qui fait des prédictions basées sur les données d’une expérience en temps réel. L’architecture actuelle n’est absolument pas capable de réaliser cela. Il faudrait pouvoir intégrer le processus de transformation des données dans l’architecture du LAAS de sorte à ne plus passer par des fichiers TDMS mais bien par les données en temps réel des capteurs.

Il faudrait utiliser cette interface comme un prototype et non comme l'aboutissement du projet.

## Contact

Si vous avez des questions ou des problèmes avec le code, je suis joignable ici : rosimon@etud.insa-toulouse.fr

