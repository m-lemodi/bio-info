# Projet Bio-Informatique : Reconstruction de novo génomes

Membres : 
* Merlin FAREZ
* Thomas SANCHEZ

# Utilisation
Pour lancer le projet, il faut éxecuter les script de la façon suivante :

**Partie 1** : Construction du graph
```bash
$ python3 debruijn_build.py source_file.fasta k_mere output_file.graph
```

**Partie 2** : Construction du graph
```bash
$ python3 debruijn_merge.py source_file.graph output_file.graph
```