# CAHIER DES CHARGES FONCTIONNEL ET TECHNIQUE
## PROJET : GÉNÉRATEUR AUTOMATISÉ DE RELEVÉS DE NOTES ET DIPLÔMES SÉCURISÉS (ZAOU-GENDOC)
### PARTIE 3 : PROTOCOLE DE RECETTE, CONTRÔLE QUALITÉ ET GUIDES D'EXPLOITATION

#### 8. PROTOCOLE DE RECETTE ET CRITÈRES D'ACCEPTATION (ACCEPTANCE CRITERIA)
Pour que la solution ZAOU-GenDoc soit officiellement déclarée conforme et prête à la production par le Secrétariat du Sénat, l'Agent IA et l'équipe technique doivent valider les quatre tests d'acceptation suivants :

##### 8.1 Test de Conformité Visuelle et Typographique
* Mise en page : Le document PDF produit doit correspondre exactement, en termes de marges, d'espacements et d'alignements, à la structure officielle des relevés historiques 2012–2017.
* Typographie : L'intégralité du texte académique doit utiliser la famille de polices Serif (Times New Roman), en respectant les graisses (gras pour les titres et décisions) et les tailles de caractères définies.
* Logo et Éléments Visuels : Le logo officiel centré en en-tête doit conserver ses proportions d'origine sans aucune déformation ni pixellisation lors de l'impression sur format A4.

##### 8.2 Test d'Integrité et de Calcul Académique
* Vérification du Cursus : Chaque relevé doit contenir la totalité des 23 modules obligatoires du Bachelor of Science in Information Technology (BIT), correctement répartis sur les 4 années académiques.
* Exactitude du GPA : Le script de calcul automatique doit déterminer sans erreur la moyenne générale (GPA) et la mention associée (Distinction, Merit, Credit, Satisfactory) à partir de la grille de conversion officielle.
* Mentions Spéciales : La ligne de décision annuelle (COMMENT : CLEAR PASS) ainsi que l'attestation finale d'attribution de diplôme doivent s'insérer dynamiquement sans chevauchement de texte.

##### 8.3 Test de Sécurité Numérique et Traçabilité
* Lisibilité du QR Code : Le QR code intégré en bas de page doit être immédiatement scannable par tout lecteur standard et renvoyer l'URL de vérification valide contenant l'identifiant de l'étudiant et son empreinte numérique.
* Calcul de l'Empreinte SHA-256 : Chaque fichier PDF généré doit avoir son empreinte binaire calculée et inscrite dans le fichier `output/audit_log.json`.
* Inviolabilité : Une modification manuelle apportée au PDF de test doit impérativement rompre la correspondance de l'empreinte SHA-256 lors de la vérification.

##### 8.4 Test de Performance et Génération par Lots (Batch Processing)
* Temps de Traitement : Le système doit être capable de générer un relevé complet de 4 ans en moins de 2 secondes par document.
* Traitement en Masse : La génération d'un lot de 50 relevés d'étudiants à partir d'un seul fichier JSON de délibération doit s'effectuer de manière autonome sans fuite de mémoire ni interruption du script.

#### 9. GUIDE DES PROCÉDURES DE CONTRÔLE QUALITÉ (QUALITY ASSURANCE MANUAL)
Le Secrétariat du Sénat applique une grille de contrôle en trois étapes avant la signature ou la délivrance officielle d'un document :

```
  [ EXTRACTION DONNÉES ]  ───►  [ GÉNÉRATION AUTOMATISÉE ]  ───►  [ AUDIT & SIGNATURE ]
  Registre Sénat (JSON)          Engine Python + Jinja2/CSS        Visualisation + Hash Audit
```

##### 9.1 Contrôle d'Entrée (Input Audit)
* Vérification que le fichier source `data/test_senate_bit_2012_2017.json` est extrait directement des registres officiels scellés par le Sénat.
* Validation que les informations de l'étudiant (Nom, Prénom, Matricule, Années d'études) ne contiennent pas de fautes de frappe.

##### 9.2 Contrôle de Sortie Visuelle (Output Visual Audit)
* Vérification de l'alignement strict de la colonne des notes (Grades) sur la marge droite.
* Contrôle de la présence explicite des deux zones de signature au bas du document (Deputy Registrar Academic et University Seal).
* Contrôle de la note de bas de page faisant référence à la grille d'évaluation située au verso.

##### 9.3 Archivage Légitime et Traçabilité (Digital Archiving)
* Stockage du PDF généré dans le répertoire sécurisé `/output/pdfs/[STUDENT_ID]_BIT_TRANSCRIPT.pdf`.
* Enregistrement systématique de la transaction d'émission dans le registre d'audit central (`output/audit_log.json`).

#### 10. DIRECTIVES D'EXÉCUTION FINALES POUR ANTIGRAVITY 2.0
Ordre Final de Déploiement :
1. Initialisation : Crée l'architecture complète des dossiers du projet (`assets/`, `data/`, `templates/`, `scripts/`, `output/`).
2. Données de Test : Génère un jeu de données JSON complet dans `data/test_senate_bit_2012_2017.json` comportant au moins 3 étudiants fictifs avec leurs 23 cours BIT étalés sur 4 ans (2012–2016 ou 2013–2017).
3. Modèles Visuels : Crée le fichier HTML `templates/transcript_2012_2017.html` et sa feuille de style CSS dédiée, en appliquant rigoureusement le style institutionnel Zambien.
4. Moteur Python : Écris les scripts nécessaires pour valider le parcours académique, générer les QR codes, compiler les templates et exporter les PDFs vectoriels au format A4 avec SHA-256.
5. Validation : Exécute le script principal, génère les documents de démonstration et confirme la bonne réussite de toutes les étapes de recette.
