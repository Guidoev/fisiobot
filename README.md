# Telegram Quiz Bot - Fisiologia

Un bot Telegram che simula un quiz di fisiologia, progettato per aiutare nella preparazione di esami in modo efficace e accessibile. Il bot utilizza un database di domande e offre diverse modalità di simulazione, fornendo un report dettagliato alla fine. 

Il progetto si basa sulla libreria [python-telegram-bot](https://python-telegram-bot.readthedocs.io/), rendendolo facile da utilizzare e disponibile ovunque tramite Telegram.

---

## Funzionalità

- **Modalità quiz**:
  - **Endless**: Rispondi a domande senza un limite, ideale per esercitarti a lungo.
  - **Simulation**: Decidi quanti quesiti vuoi affrontare (15, 25, 35, 45, 60, 100).
- **Report**: Al termine del quiz, ricevi un riepilogo con il numero di risposte corrette, errate e percentuale di successo.
- **Portabilità**: Funzionando tramite Telegram, puoi usarlo ovunque, da qualsiasi dispositivo.

---

## Motivazione

Questo bot è stato creato per aiutare un amico a prepararsi all'esame di fisiologia. Il materiale di studio disponibile era poco formattato e difficile da consultare. Grazie al bot, il processo di esercitazione è diventato molto più semplice, portando al superamento dell'esame con successo.

---

## Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-username/telegram-quiz-bot.git
   cd telegram-quiz-bot
   ```

2. Installa le dipendenze richieste:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura il bot:
   - Ottieni un token API da [BotFather](https://core.telegram.org/bots#botfather) su Telegram.
   - Inserisci il token nel file di configurazione (`config.py`) o come variabile d'ambiente.

4. Avvia il bot:
   ```bash
   python bot.py
   ```

---

## Requisiti

- Python 3.8 o superiore
- Libreria `python-telegram-bot`
- Un token API Telegram

---

## Screenshot

<p align="center">
  <img src="/examples/questions.jpeg" alt="Selezione del numero di domande della simulazione" width="30%" style="display:inline-block; margin-right: 10px;">
  <img src="/examples/tf.jpeg" alt="Esempio di domanda" width="30%" style="display:inline-block;">
  <img src="/examples/recap.jpeg" alt="Riepilogo di fine test" width="30%" style="display:inline-block;">
</p>

---

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Consulta il file `LICENSE` per maggiori dettagli.

---

## Contributi

Contributi, segnalazioni di bug e suggerimenti sono benvenuti! Sentiti libero di aprire una [issue](https://github.com/tuo-username/telegram-quiz-bot/issues) o creare una pull request.

---

### Nota finale

Grazie per aver utilizzato Telegram Quiz Bot! Spero possa essere utile per il tuo studio e per superare con successo i tuoi esami.
