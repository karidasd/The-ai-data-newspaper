<p align="center">
  <img src="logo.png" width="250" alt="The AI & Data Newspaper Logo">
</p>

# The AI & Data Newspaper 🤖📰
[![GitHub Pages](https://img.shields.io/badge/Deployed_on-GitHub_Pages-blue)](https://karidasd.github.io/The-ai-data-newspaper/)

*[🇬🇧 English version below]*

Αυτό το αποθετήριο δημιουργεί αυτόματα ένα **πανέμορφο ψηφιακό περιοδικό** με τα τελευταία νέα από τον χώρο της Τεχνητής Νοημοσύνης και της Επιστήμης Δεδομένων.

Χρησιμοποιεί **Python** και **GitHub Actions** για να συλλέγει άρθρα μέσω RSS feeds κάθε Παρασκευή, δημιουργώντας αυτόματα μια στατική ιστοσελίδα (`index.html`) με κλασικό, editorial design!

## 🚀 Πώς Λειτουργεί
1. Ένα GitHub Action εκτελείται αυτόματα κάθε Παρασκευή στις 08:00 UTC.
2. Τρέχει το αρχείο `generate_newsletter.py`.
3. Το script διαβάζει τα τελευταία RSS feeds από κορυφαίες πηγές (MIT News, Towards Data Science, KDNuggets, Google AI Blog).
4. Παράγει ένα ολοκαίνουριο `index.html` με μοντέρνο CSS (χωρίς εξωτερικές εξαρτήσεις).
5. Το GitHub κάνει commit, push και ανανεώνει το GitHub Pages αυτόματα!

Μπορείτε να δείτε το περιοδικό live εδώ: **[The AI & Data Newspaper](https://karidasd.github.io/The-ai-data-newspaper/)**

---

## 🇬🇧 English

This repository automatically generates a **beautiful digital magazine** featuring the latest news in Artificial Intelligence and Data Science.

It uses **Python** and **GitHub Actions** to aggregate articles via RSS feeds every Friday, automatically building a static website (`index.html`) with a classic editorial design!

## 🚀 How it Works
1. A GitHub Action runs automatically every Friday at 08:00 UTC.
2. It executes the `generate_newsletter.py` script.
3. The script fetches the latest RSS feeds from top sources (MIT News, Towards Data Science, KDNuggets, Google AI Blog).
4. It generates a brand new `index.html` with modern, vanilla CSS.
5. GitHub automatically commits, pushes the changes, and deploys to GitHub Pages!

You can view the live magazine here: **[The AI & Data Newspaper](https://karidasd.github.io/The-ai-data-newspaper/)**
