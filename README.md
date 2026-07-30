# ZAOU-GenDoc — Générateur Automatisé de Relevés de Notes et Diplômes Sécurisés

**Zambian Open University (ZAOU) — Office of the Senate Secretariat**

---

## Description

**ZAOU-GenDoc** est le système officiel d'automatisation de génération des Relevés de Notes (Official Transcripts) et des E-Documents certifiés de la **Zambian Open University (ZAOU)**. Développé et déployé par **Antigravity 2.0** sous la directive du Secrétariat du Sénat académique, ce pipeline produit instantanément des documents académiques irréprochables à partir des données de délibération brutes du Sénat.

**Programme Pilote** : Bachelor of Science in Information Technology (BIT) — Cohorte 2012–2017

---

## Architecture du Projet

```
zaou-gendoc/
├── assets/
│   ├── zaou_logo.png                # Logo officiel ZAOU extrait des archives
│   ├── registrar_signature.png       # Signature du Deputy Registrar (Academic)
│   └── university_seal.png           # Sceau officiel Academic Affairs (violet)
│
├── data/
│   └── test_senate_bit_2012_2017.json  # 50 dossiers étudiants BIT (registre Sénat)
│
├── templates/
│   ├── transcript_2012_2017.html    # Template Jinja2 (Page 1 Recto + Page 2 Verso)
│   └── styles.css                   # Feuille de style A4 (Times New Roman, print media)
│
├── scripts/
│   ├── generate_test_data.py        # Génération du registre de délibération (JSON)
│   ├── generate_assets.py           # Génération du sceau et de la signature
│   ├── validate_data.py             # Audit des 23 matières BIT + calcul GPA
│   ├── generate_qr.py               # QR code d'authentification dynamique
│   └── generate_pdf.py              # Pipeline principal : Jinja2 → WeasyPrint → PDF + SHA-256
│
├── output/
│   ├── pdfs/                        # PDFs générés : [STUDENT_ID]_BIT_TRANSCRIPT.pdf
│   └── audit_log.json               # Registre cryptographique SHA-256
│
├── CAHIER_DES_CHARGES_PARTIE_1.md   # Spécifications visuelles et institutionnelles
├── CAHIER_DES_CHARGES_PARTIE_2.md   # Cursus BIT 2012-2017 et architecture technique
└── CAHIER_DES_CHARGES_PARTIE_3.md   # Protocole de recette, QA et guides d'exploitation
```

---

## Prérequis

```bash
pip install weasyprint qrcode reportlab jinja2 pillow cryptography
```

---

## Utilisation

### Étape 1 — Générer les données de test (registre Sénat)
```bash
python3 scripts/generate_test_data.py
```
Génère `data/test_senate_bit_2012_2017.json` contenant 50 dossiers étudiants complets.

### Étape 2 — Valider l'intégrité du registre
```bash
python3 scripts/validate_data.py
```
Vérifie que chaque étudiant possède les **23 matières BIT obligatoires** et calcule les GPA.

### Étape 3 — Lancer la génération complète des PDFs
```bash
python3 scripts/generate_pdf.py
```
- Compile les templates Jinja2 avec les données de chaque étudiant.
- Génère 50 PDFs vectoriels A4 dans `output/pdfs/`.
- Enregistre les empreintes SHA-256 dans `output/audit_log.json`.

---

## Structure d'un Relevé Officiel Généré

**Page 1 (Recto — Front Side)**
| Zone | Contenu |
|---|---|
| En-tête | Logo ZAOU + "THE ZAMBIAN OPEN UNIVERSITY / OFFICE OF THE DEPUTY REGISTRAR" |
| Bio Data | "This is to certify that [NOM] Student Identity Number [MATRICULE] was a registered student…" |
| Résultats | 4 blocs annuels (FIRST–FOURTH YEAR), 3 colonnes épurées : Code — Intitulé — Grade |
| Décisions | `COMMENT : CLEAR PASS` après chaque année |
| Attestation | "HE/SHE WAS AWARDED THE DEGREE OF BSc IT WITH [DISTINCTION/MERIT/CREDIT]…" |
| Légalisation | Signature Deputy Registrar + Sceau University Seal + QR Code dynamique |
| Pied de page | *"NB : A key to the understanding of the grade is on the reverse side of this sheet."* |

**Page 2 (Verso — Reverse Side)**
- Grille officielle ZAOU des notes (A+ à D, codes spéciaux P, S, EX, INC)
- Notice d'inviolabilité institutionnelle

---

## Sécurité et Traçabilité

| Mécanisme | Détail |
|---|---|
| QR Code dynamique | URL `https://verify.zaou.ac.zm/transcript?student_id=...&hash=...` |
| Empreinte SHA-256 | Hash binaire du PDF → inscrit dans `output/audit_log.json` |
| Méta-données PDF | Auteur, Sujet, Copyright injectés automatiquement |
| Inviolabilité | Toute modification du PDF invalide l'empreinte SHA-256 |

---

## Échelle de Notation ZAOU (2012–2017)

| % | Grade | Classification |
|---|---|---|
| 86–100 | A+ | Distinction |
| 76–85 | A | Distinction |
| 68–75 | B+ | Meritorious |
| 62–67 | B | Very Satisfactory |
| 56–61 | C+ | Definite Pass |
| 50–55 | C | Bare Pass |
| 40–49 | D+ | Bare Fail |
| 0–39 | D | Clear Fail |

---

## Résultats des Tests de Recette (Partie 3)

| Test | Résultat |
|---|---|
| 8.1 — Conformité Visuelle & Typographique | ✅ PASSED |
| 8.2 — Intégrité Académique & Calcul GPA | ✅ PASSED |
| 8.3 — Sécurité Numérique & SHA-256 | ✅ PASSED |
| 8.4 — Performance & Traitement par Lots | ✅ PASSED (0.648s/doc) |
| **Verdict Final** | **✅ SYSTÈME APPROUVÉ POUR LA PRODUCTION** |

---

## Autorité d'Émission

> **Office of the Senate Secretariat — Zambian Open University**
> Office of the Deputy Registrar (Academic Affairs)
> P.O. Box — Lusaka, Zambia
> `academic-office@zaou.ac.zm`

---

*© Zambian Open University — All Rights Reserved. ZAOU-GenDoc, Antigravity 2.0.*
