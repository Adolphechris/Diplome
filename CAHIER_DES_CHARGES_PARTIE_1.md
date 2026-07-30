# CAHIER DES CHARGES FONCTIONNEL ET TECHNIQUE
## PROJET : GÉNÉRATEUR AUTOMATISÉ DE RELEVÉS DE NOTES ET DIPLÔMES SÉCURISÉS (ZAOU-GENDOC)
### PARTIE 1 : INSTITUTION, CONTEXTE ACADÉMIQUE ET SPÉCIFICATIONS VISUELLES

#### 1. PRÉSENTATION DE L'INSTITUTION ET DE L'AUTORITÉ D'ÉMISSION
##### 1.1 La Zambian Open University (ZAOU)
La Zambian Open University (ZAOU) est une institution d'enseignement supérieur de premier plan en Zambie, reconnue pour son excellence dans la dispensation de programmes académiques à distance, ouverts et en présentiel. Fondée avec la mission d'élargir l'accès à un enseignement supérieur de qualité, la ZAOU est dûment enregistrée et accréditée par la Higher Education Authority (HEA) ainsi que par la Zambia Qualifications Authority (ZAQA).

##### 1.2 Le Secrétariat du Sénat (Office of the Senate Secretariat)
Au cœur de la gouvernance académique de la ZAOU se trouve le Sénat académique, dont le Secrétariat assure la garde et l'administration des décisions académiques. Le Secrétariat du Sénat, en collaboration étroite avec le Bureau du Registre Adjoint aux Affaires Académiques (Office of the Deputy Registrar - Academic Affairs), est l'unique autorité légale et administrative habilitée à :
* Sanctionner la réussite des étudiants et approuver les procès-verbaux de délibération des examens.
* Autoriser l'attribution des grades universitaires, des diplômes et des certificats.
* Émettre, signer, sceller et archiver les relevés de notes officiels (Official Transcripts) et les parchemins de diplôme (Degree Certificates).
* Répondre aux requêtes de vérification d'authenticité émanant des employeurs, des institutions partenaires et des organismes gouvernementaux tels que la ZAQA.

#### 2. CONTEXTE STRATÉGIQUE ET OBJECTIFS DU PROJET
##### 2.1 Contexte de la Modernisation
Afin d'absorber la croissance du nombre de diplômés et de répondre aux exigences de réactivité modernes sans compromettre la sécurité, le Secrétariat du Sénat initie la numérisation et l'automatisation avancée de son processus d'édition de documents. Le projet ZAOU-GenDoc vise à déployer un pipeline autonome local, opérant dans un environnement de développement agentique moderne (Antigravity 2.0), capable de générer instantanément des documents académiques irréprochables à partir des données de délibération brutes du Sénat.

##### 2.2 Périmètre Académique et Historique (Phase Pilote)
La première phase du projet cible une fenêtre historique précise :
* Période cible : Cursus académiques suivis et complétés entre les années 2012 et 2017 incluses.
* Programme Pilote : Le programme d'études retenu est le Bachelor of Science in Information Technology (BIT), relevant de la Faculté des Sciences Humaines et Appliquées (School of Humanities and Social Sciences).
* Format des Cursus : Programme de premier cycle (Undergraduate) s'étalant sur quatre années académiques (8 semestres), caractérisé par un parcours progressif allant des fondamentaux informatiques jusqu'au projet de fin d'études.

##### 2.3 Objectifs Globaux du Système
* Fidélité Historique Absolue : Reproduire au millimètre près l'esthétique, la typographie, les alignements et la mise en page des documents imprimés par la ZAOU durant la période 2012–2017, en se basant sur les standards nationaux de l'enseignement supérieur zambien.
* Élimination Totale de la Saisie Manuelle : Extraire automatiquement les données depuis les registres validés par le Sénat, prévenant ainsi toute erreur matérielle sur les noms, matricules, codes de cours ou notes.
* Double Format de Sortie : Produire simultanément un document PDF haute résolution prêt pour l'impression physique officielle sur papier sécurisé, et un document électronique certifié (E-Transcript / E-Degree) doté d'empreintes numériques et de mécanismes de vérification en ligne.

#### 3. SPÉCIFICATIONS VISUELLES ET GRAPHILOGIQUES RIGOUREUSES
Le générateur développé par Antigravity 2.0 doit appliquer une restitution visuelle d'une précision chirurgicale, découpée en plusieurs zones distinctes sur le document :

##### 3.1 En-tête Institutionnel (Header Section)
* Logo Officiel : Le logo circulaire officiel de la Zambian Open University doit être positionné au centre supérieur de la page. Il présente le motif d'œil stylisé bordé d'orange, le chapeau de diplômé bleu sur livre ouvert, et la bande circulaire bleue portant la mention "ZAMBIAN OPEN UNIVERSITY".
* Bloc Textuel Administratif : Placé directement sous le logo, centré, en lettres majuscules d'une police Serif académique classique (Times New Roman) :
  * Première ligne : THE ZAMBIAN OPEN UNIVERSITY
  * Deuxième ligne : OFFICE OF THE DEPUTY REGISTRAR
  * Troisième ligne : P.O. BOX LUSAKA - ZAMBIA
  * Quatrième ligne (coordonnées) : Téléphone, télécopie et adresse e-mail officielle de l'Academic Office.
* Titre du Document : Intitulé en caractères gras, taille augmentée et centré : OFFICIAL TRANSCRIPT.

##### 3.2 Attestation d'Identité et de Parcours (Student Bio Data)
Sous l'en-tête, un paragraphe rédigé en prose institutionnelle juste et formelle atteste de l'inscription de l'étudiant. Il doit impérativement adopter la formulation zambienne standard :
"This is to certify that [NOM ET PRÉNOMS DE L'ÉTUDIANT] Student Identity Number [MATRICULE] was a registered student of The Zambian Open University in the School of Humanities and Social Sciences during the Academic Session(s) [ANNÉE DE DÉBUT - ANNÉE DE FIN]."

##### 3.3 Présentation des Résultats par Année Académique (Academic Performance Layout)
Contrairement aux tableaux modernes fermés par d'épaisses bordures, le style classique 2012–2017 utilise une présentation épurée par blocs annuels, séparés par de fines lignes horizontales :
* En-tête d'Année : Chaque section débute par l'année et le niveau, affichés en gras et majuscules (ex : 2012 - FIRST YEAR, 2013 - SECOND YEAR, 2014 - THIRD YEAR, 2015 - FOURTH YEAR).
* Alignement des Cours : Pour chaque année, la liste des matières est structurée en trois colonnes parfaitement alignées horizontalement :
  * Colonne de gauche : Le code officiel du cours (ex : BIT 110).
  * Colonne centrale : L'intitulé complet de la matière académique (ex : Introduction to Information Technology).
  * Colonne de droite : La note alphabétique obtenue (Grade) alignée sur la marge droite (ex : A+, B+, C).
* Décision Annuelle du Sénat : À la fin de la liste des cours de chaque année académique, une ligne de décision explicite est inscrite en majuscules soulignées ou en gras (ex : COMMENT : CLEAR PASS).

##### 3.4 Décision Finale et Attribution du Grade (Graduation Statement)
À la suite de la quatrième année, le document doit afficher la décision finale d'attribution du diplôme approuvée par le Sénat :
"HE / SHE WAS AWARDED THE DEGREE OF BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY WITH [MENTION : DISTINCTION / MERIT / CREDIT / SATISFACTORY] AT THE GRADUATION CEREMONY HELD IN LUSAKA."

##### 3.5 Zone de Validation, Signatures et Sceau (Validation & Signatures)
En bas de la page, le document réserve les espaces officiels de légalisation :
* Signature de Marge Gauche : Intitulée DEPUTY REGISTRAR (ACADEMIC), surmontée de l'emplacement de la signature manuscrite ou numérique certifiée.
* Sceau Officiel Central/Droit : Un espace dédié estampillé du sceau de l'université (UNIVERSITY SEAL / ACADEMIC AFFAIRS STAMP), représenté en violet/bleu nuit ou rouge institutionnel.
* Dispositif de Sécurité Numérique : Intégration dans le coin inférieur d'un QR code de vérification dynamique, discret mais parfaitement scannable.
* Note de bas de page (Footer Legend) : Inscription obligatoire en italique : "NB : A key to the understanding of the grade is on the reverse side of this sheet."
