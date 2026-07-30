# CAHIER DES CHARGES FONCTIONNEL ET TECHNIQUE
## PROJET : GÉNÉRATEUR AUTOMATISÉ DE RELEVÉS DE NOTES ET DIPLÔMES SÉCURISÉS (ZAOU-GENDOC)
### PARTIE 2 : MAQUETTE DE CURSUS BIT (2012–2017), ARCHITECTURE TECHNIQUE ET SÉCURITÉ

#### 4. STRUCTURE DÉTAILLÉE DU PROGRAMME PILOTE : BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY (2012–2017)
Pour garantir une fidélité académique absolue, le générateur doit injecter la grille exacte des cours du programme Bachelor of Science in Information Technology (BIT) dispensé par la ZAOU durant la période 2012–2017. Le cursus est structuré en quatre années (huit semestres) d'apprentissage progressif :

##### 4.1 Première Année (First Year) — Fondations Informatiques et Générales
* BIT 110 : Introduction to Information Technology (Fondements des technologies de l'information, matériel et logiciel)
* BIT 111 : Fundamentals of Computer Programming (Initiation à la logique de programmation et algorithmique de base)
* MA 110 : Mathematics for Computing I (Algèbre, analyse et mathématiques appliquées aux systèmes)
* LA 111 : Communication and Academic Writing Skills (Techniques d'expression, de rédaction académique et de rapport)
* BIT 120 : Computer Systems and Architecture (Structure interne des ordinateurs, processeurs et mémoire)
* MA 120 : Discrete Mathematics for IT (Logique booléenne, théorie des graphes et ensembles)
* Décision Annuelle : COMMENT : CLEAR PASS

##### 4.2 Deuxième Année (Second Year) — Développement, Réseaux et Bases de Données
* BIT 210 : Object-Oriented Programming (Programmation orientée objet avancée en Java ou C++)
* BIT 211 : Database Management Systems (Conception, modélisation relationnelle et langage SQL)
* BIT 220 : Data Structures and Algorithms (Structures de données complexes, tri, recherche et optimisation)
* BIT 221 : Systems Analysis and Design (Méthodologies d'analyse de systèmes d'information, UML et cycles de vie)
* BIT 222 : Web Technologies and Applications (Développement d'applications web, HTML, CSS, JavaScript et scripts serveur)
* BIT 223 : Computer Networks I (Architecture réseau, modèle OSI, protocole TCP/IP et routage)
* Décision Annuelle : COMMENT : CLEAR PASS

##### 4.3 Troisième Année (Third Year) — Ingénierie Logicielle, Sécurité et Gestion IT
* BIT 310 : Operating Systems Concepts (Principes des systèmes d'exploitation, gestion des processus et de la mémoire)
* BIT 311 : Software Engineering Principles (Génie logiciel, gestion de projet agile, tests et qualité)
* BIT 320 : Computer Networks II & Security (Administration de réseaux avancée, pare-feu et sécurité des communications)
* BIT 321 : Management Information Systems (Systèmes d'information de gestion d'entreprise, ERP et prise de décision)
* BIT 322 : IT Project Management (Gestion de projets informatiques, planification, coûts et risques)
* BIT 323 : Research Methods in IT (Méthodologie de la recherche scientifique appliquée aux technologies)
* Décision Annuelle : COMMENT : CLEAR PASS

##### 4.4 Quatrième Année (Fourth Year) — Spécialisation et Projet de Fin d'Études
* BIT 410 : Information Security and Cryptography (Sécurité des données, chiffrement, PKI et cyberdéfense)
* BIT 411 : Distributed Systems & Cloud Computing (Calcul distribué, architectures microservices et cloud)
* BIT 420 : Wireless and Mobile Computing (Technologies mobiles, réseaux sans fil et développement d'applications embarquées)
* BIT 421 : E-Commerce and Enterprise Systems (Systèmes e-business, transactions sécurisées et intégration applicative)
* BIT 400 : Final Year IT Project / Capstone Dissertation (Projet de fin d'études pratique et rédaction de mémoire devant jury)
* Décision Annuelle : COMMENT : CLEAR PASS

##### 4.5 Échelle Officielle d'Évaluation des Notes (Verso du Relevé / Page 2 Legend)
Le verso du document ou la deuxième page du template doit obligatoirement inclure l'échelle officielle d'évaluation en vigueur à la ZAOU pour la période 2012–2017 :
* 86% – 100% : A+ (Distinction)
* 76% – 85% : A (Distinction)
* 68% – 75% : B+ (Meritorious)
* 62% – 67% : B (Very Satisfactory)
* 56% – 61% : C+ (Definite Pass)
* 50% – 55% : C (Bare Pass)
* 40% – 49% : D+ (Bare Fail)
* 0% – 39% : D (Clear Fail)
* Symboles Spéciaux : P (Pass in Supplementary Exam), S (Successfully Completed Industrial Attachment), EX (Exemption), INC (Incomplete).

#### 5. SPÉCIFICATIONS TECHNIQUES DU MOTEUR DU GÉNÉRATEUR (BACKEND LOGIC)
L'Agent IA dans Antigravity 2.0 doit programmer le moteur backend en Python selon les principes de conception suivants :

##### 5.1 Validation de la Cohérence des Données (Data Validation Engine)
Avant tout rendu visuel, le moteur extrait le fichier de délibération du Sénat (format JSON ou Excel) et procède à un audit logique strict :
* Vérification du Matricule : Contrôle du format de l'identifiant étudiant (Student Identity Number).
* Vérification du Cursus : Contrôle de l'exhaustivité des 23 modules obligatoires du programme BIT.
* Calcul automatique de la Mention Finale : Si les notes individuelles sont valides, le script évalue la moyenne pondérée (Grade Point Average - GPA) pour déterminer dynamiquement la mention académique à inscrire sur l'attestation :
  * Distinction (GPA supérieur ou égal à 3.60)
  * Merit (GPA compris entre 3.00 et 3.59)
  * Credit (GPA compris entre 2.50 et 2.99)
  * Satisfactory / Pass (GPA compris entre 2.00 et 2.49)

##### 5.2 Rendu HTML/CSS et Conversion PDF Vectoriel
* Compilation Jinja2 : Les données de chaque étudiant sont fusionnées avec le modèle HTML templates/transcript_2012_2017.html.
* Rendu Média d'Impression (CSS Print Media) : Le fichier CSS associé définit un format de page A4 strict (`@page { size: A4; margin: 15mm; }`), gère les sauts de page contrôlés (`page-break-inside: avoid;`), garantit l'ancrage du bloc de signatures au bas de la page et la netteté vectorielle de la police Times New Roman à 300 DPI.
* Génération PDF headless : Utilisation d'un moteur de rendu Chromium / WeasyPrint pour exporter le fichier PDF sans aucune déformation de la mise en page originale.

#### 6. MODULE DE SÉCURITÉ ET NORMES "E-DOCUMENT" (ÉLECTRONIQUE)
Pour transformer chaque document physique en un E-Document certifié, le système intègre un triple niveau de protection cryptographique :

##### 6.1 QR Code Dynamique d'Authenticité
* Un QR code est généré pour chaque étudiant à l'aide de la bibliothèque Python qrcode.
* Le QR code contient une URL sécurisée vers le portail de vérification du Secrétariat : `https://verify.zaou.ac.zm/transcript?student_id=[MATRICULE]&hash=[HASH_SHA256]`
* Le QR code est automatiquement incrusté dans le template HTML en bas à droite avant la conversion PDF.

##### 6.2 Scellement par Empreinte Cryptographique (SHA-256)
* Dès que le PDF est généré, le script calcule l'empreinte numérique unique (Hash SHA-256) du fichier binaire.
* Cette empreinte est enregistrée dans un registre d'audit local (`output/audit_log.json`). Toute altération ultérieure du PDF modifiera la clé binaire et rendra le document invalide.

##### 6.3 Métadonnées Institutionnelles
Le script injecte dans l'en-tête interne du fichier PDF les métadonnées officielles :
* Auteur : Office of the Senate Secretariat - Zambian Open University
* Sujet : Official Academic Transcript - Bachelor of Science in Information Technology
* Droits d'auteur : Zambian Open University (All Rights Reserved)
