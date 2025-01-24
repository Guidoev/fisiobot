import logging
import json
import random
from typing import Dict
import telegram
import telegram._bot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

#-----------------------------------------------------------------------------------------------------------------------

class Question:
    def __init__(self, contesto: str, domanda: str, risposta: bool, spiegazione: str = None):
        self.contesto = contesto
        self.domanda = domanda
        self.risposta = risposta
        self.spiegazione = spiegazione

def loadQuestions(file_path):
    # Carica il file JSON
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)

    questions = []

    # Itera sui dati e crea le domande
    for item in data:
        contesto = item.get('contesto', None)
        domanda = item.get('domanda', '')
        risposta = item.get('risposta', '')
        spiegazione = item.get('spiegazione', None)

        # Crea l'oggetto Question e lo aggiunge alla lista
        question = Question(contesto, domanda, risposta, spiegazione)
        questions.append(question)

    return questions

def printQuestion(user_data) -> str:
    domanda = f"<code>\n• Domanda {user_data['done'] + 1 + (user_data['prestige']*TOT if user_data['choice'] == 'Endless' else 0)}</code>"
    domanda += f"<code>/{user_data['qty']} - ({'{:.2f}'.format(user_data['done'] / float(user_data['qty']) * 100)}%)</code>\n" if user_data['choice'] == "Simulation" else "\n"
    domanda += f"<code>\n{user_data['db'][user_data['done']].contesto}\n</code>" if user_data["db"][user_data["done"]].contesto is not None else "\n<code>Nessun contesto disponibile</code>\n"
    domanda += f"\n{user_data['db'][user_data['done']].domanda}"
    return domanda

#-----------------------------------------------------------------------------------------------------------------------

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------------------------------------------------------

CHOOSING, AMOUNT, QUESTIONS = range(3)

TOT = 1014

start_keyboard = [["/start"]]
markupS = ReplyKeyboardMarkup(start_keyboard)

menu_keyboard = [["Simulation", "Endless", "Termina"]]
markupM = ReplyKeyboardMarkup(menu_keyboard)

qty_keyboard = [["15", "25", "35"],["45", "60", "100"]]
markupN = ReplyKeyboardMarkup(qty_keyboard)

question_keyboard = [["Vero", "Falso"], ["Interrompi"]]
markupQ = ReplyKeyboardMarkup(question_keyboard)

#-----------------------------------------------------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Ciao, sei pronto a passare l'esame?", parse_mode=telegram.constants.ParseMode.HTML, reply_markup=markupM,)
    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data

    choice = update.message.text

    user_data["choice"] = choice

    if choice != "Termina":
        user_data["db"] = loadQuestions("domande.json")
        random.shuffle(user_data["db"])
    else:
        print("Sono in regular_choice")

    user_data["done"] = 0
    user_data["correct"] = 0

    if choice == "Endless":
        user_data["prestige"] = 0
        await update.message.reply_text("<b>Inizio Modalità Endless</b>\n\n<code>---------------------------------</code>\n\n" + printQuestion(user_data), parse_mode=telegram.constants.ParseMode.HTML, reply_markup=markupQ)
        return QUESTIONS
    else:
        await update.message.reply_text("Quante Domande?", parse_mode=telegram.constants.ParseMode.HTML, reply_markup=markupN)
        return AMOUNT

async def question_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data

    user_data["qty"] = update.message.text

    await update.message.reply_text(f"<b>Inizio Simulazione ({user_data['qty']} Domande)</b>\n\n<code>---------------------------------</code>\n\n" + printQuestion(user_data), parse_mode=telegram.constants.ParseMode.HTML, reply_markup=markupQ)
    return QUESTIONS




async def main_loop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data

    answer = update.message.text

    if answer == "Interrompi":
        text = f"<code>------------ report -------------\nDomande fatte: {user_data['done'] + (user_data['prestige']*TOT if user_data['choice'] == 'Endless' else 0)}\nRisposte Corrette: {user_data['correct']}\nPercentuale di successo: {('{:.2f}'.format(user_data['correct']/float(user_data['done'] + (user_data['prestige']*TOT if user_data['choice'] == 'Endless' else 0))*100))if user_data['done'] > 0 else 0}%\n---------------------------------</code>\n"
        user_data.clear()
        await update.message.reply_text(text, parse_mode=telegram.constants.ParseMode.HTML, reply_markup=markupM)
        return CHOOSING

    #imposta emoji

    if user_data["db"][user_data["done"]].risposta == "?":
        text = "<b>RISPOSTA NON PRESENTE NEL DB - VAI A CONTROLLARE</b>\nPer la simulazione è considerata corretta"
        user_data["correct"] += 1
    elif user_data["db"][user_data["done"]].risposta == answer:
        text = u'✅' + " <b>CORRETTO!!</b>" + u'✅'
        user_data["correct"] += 1
    else:
        text = u'❌' + " <b>SBAGLIATO</b>" + u'❌'

    text += f"\n\n<b>Spiegazione:</b> {user_data['db'][user_data['done']].spiegazione if user_data['db'][user_data['done']].spiegazione is not None else 'nessuna'}\n"

    user_data["done"] += 1

    if user_data["choice"] == "Simulation":
        if user_data["done"] >= int(user_data["qty"]):
            text += f"\n\n<code>------------- report ------------\nDomande fatte: {user_data['done']}\nRisposte Corrette: {user_data['correct']}\nPercentuale di successo: {'{:.2f}'.format(user_data['correct']/float(user_data['done'])*100)}%\n---------------------------------</code>\n"
            user_data.clear()
            await update.message.reply_text(text, parse_mode=telegram.constants.ParseMode.HTML, reply_markup=markupM)
            return CHOOSING
        else:
            text += "<code>---------------------------------</code>\n"
    else:
        text += f"\n\n<code>--------- partial report --------\nDomande fatte: {user_data['done'] + (user_data['prestige']*TOT)}\nRisposte Corrette: {user_data['correct']}\nPercentuale di successo: {'{:.2f}'.format(user_data['correct'] / float(user_data['done'] + (user_data['prestige']*TOT))*100)}%\n---------------------------------</code>\n"
        if user_data["done"] >= TOT:
            user_data["prestige"] += 1
            user_data["done"] = 0
            random.shuffle(user_data["db"])

    await update.message.reply_text(text + printQuestion(user_data), parse_mode=telegram.constants.ParseMode.HTML, reply_markup=markupQ)
    return QUESTIONS

#-----------------------------------------------------------------------------------------------------------------------

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user_data = context.user_data
    user_data.clear()

    await update.message.reply_text("Termino FisioBot", reply_markup=markupS)

    return ConversationHandler.END



def main() -> None:

    # Create the Application and pass it your bot's token.
    application = Application.builder().token("[insert-your-API-key-here]").build()


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],

        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^(Simulation|Endless)$"), regular_choice)
            ],
            AMOUNT: [
                MessageHandler(filters.Regex("^(15|25|35|40|60|100)$"), question_choice)
            ],
            QUESTIONS: [
                MessageHandler(filters.Regex("^(Vero|Falso|Interrompi)$"), main_loop)
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Termina$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()