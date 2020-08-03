# This Python file uses the following encoding: utf-8

import os
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, Filters,  CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler
import logging

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

categories = ['Filmes', 'Séries', 'Shows', 'Jogos', 'Livros e Literatura',
              'Beleza e Fitness', 'Idiomas', 'Ciência e Ensino (tópicos acadêmicos)',
              'Hardware', 'Software', 'Esportes', 'Dança', 'Música', 'Pintura e Desenho',
              'Culinária', 'Mão na massa (consertos, costura, tricô, etc.)', 'Casa e Jardim',
              'Pets', 'Compras', 'Trabalho voluntário', 'Hobbies e Lazer', 'Política',
              'Finanças', 'Viagens e Turismo', 'Intercâmbio', 'Automóveis e Veículos',
              'Esotérico e Holístico', 'Espiritualidade', 'Times do coração',
              'Causas (ambientais, feminismo, vegan, etc.)', 'Moda',
              'Empreenderismo e Negócios', 'Imobiliário', 'Artesanato', 'Fotografia',
              'História', 'Mitologia', 'Pessoas e Sociedade', 'Anime e Mangá']

# Give each category an ID
categories = enumerate(categories)


def normalizeCategories(categories, num_per_row=1):
    new_categories = []
    new_row = []
    for id, cat in categories:
        if id > 0 and id % num_per_row == 0:  # start a new row
            new_categories.append(new_row[:])  # makes a copy
            new_row = []
            new_row.append((id, cat))
        else:
            new_row.append((id, cat))
    return new_categories


norm_categories = normalizeCategories(categories, 1)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.getLogger(__name__)

# Define o nosso BD de teste
BD = {}

# States
REGISTER_NAME, REGISTER_BIO, CHOOSE_ACTION = range(3)
# States for interests conversation
CHOOSING = 3


# start => Inicia o bot. Se a pessoa não estiver cadastrada na base de dados
# (dá pra ver pelo ID do Tele), pede para ela fornecer
# um nome, uma pequena descrição pessoal e, por último para escolher seus interesses iniciais.

def help(update, context):
    text = "/prefs - Retorna uma lista com todas as categorias de interesse. A partir dela que você poderá adicionar ou remover interesses.\n"
    text += "/show - Mostra uma pessoa que tem interesses em comum.\n"
    text += "/random - Mostra uma pessoa aleatória.\n"
    text += "/pending - Mostra todas as solicitações de conexão que você possui e ainda não respondeu.\n"
    text += "/friends - Mostra o contato de todas as pessoas com que você já se conectou.\n"
    text += "/help - Mostra novamente essa lista. Alternativamente, você pode digitar \"/\" e a lista de comando também aparecerá!"
    update.message.reply_text(text)
    return CHOOSE_ACTION


def start(update, context):
    # Checa se o usuário já está no BD
    if update.effective_user.id in BD:
        update.message.reply_text(
            "Bora começar a usar o aplicativo!\nMe diz: o que você quer fazer agora? :)\n")
        help(update, context)

    # Caso contrario, o usuario devera se registrar
    update.message.reply_text(
        'Parece que você não está registrado no Approxima ainda...\nPor favor, me forneça o seu nome! (ex: Joao Vitor dos Santos)')
    return REGISTER_NAME


def register_name(update, context):
    response = f"Seu nome é:\n \"{update.message.text}\".\n\n"
    response += "Legal! Agora, me conte um pouco mais sobre seus gostos... Usaremos essa descrição para te apresentar para os outros usuários do Approxima."

    update.message.reply_text(response)
    context.user_data['name'] = update.message.text
    return REGISTER_BIO


def register_bio(update, context):
    update.message.reply_text(
        f"Sua mini bio é:\n \"{update.message.text}\".\n\nBoa! Agora só falta você adicionar alguns interesses para começar a usar o app!\nClique aqui --> /prefs")
    context.user_data['bio'] = update.message.text

    # Comeca elx com 0 categorias selecionadas
    context.user_data['interests'] = []

    # Joga as informacoes no BD
    BD[update.effective_user.id] = context.user_data
    return CHOOSE_ACTION

    # prefs => Retorna lista de interesses (caixa de seleção). A pessoa pode marcar
    # ou desmarcar o que ela quiser.


def prefs(update, context):
    cats = context.user_data['interests']

    keyboard = [
        [
            InlineKeyboardButton("☑ " + cat, callback_data=str(id)) if id in cats
            else InlineKeyboardButton(cat, callback_data=str(id))
            for id, cat in row
        ]
        for row in norm_categories
    ]
    keyboard.append([InlineKeyboardButton("ENVIAR", callback_data="finish")])

    update.message.reply_text(
        'Escolha suas categorias de interesse:', reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSING


def mark_category(update, context):
    update.callback_query.answer()  # await for answer

    cats = context.user_data['interests']

    # Trata a resposta anterior
    data_id = int(update.callback_query.data)
    if data_id in cats:
        cats.remove(data_id)
    else:
        cats.append(data_id)

    # Constroi o novo teclado
    keyboard = [
        [
            InlineKeyboardButton("☑ " + cat, callback_data=str(id)) if id in cats
            else InlineKeyboardButton(cat, callback_data=str(id))
            for id, cat in row
        ]
        for row in norm_categories
    ]
    keyboard.append([InlineKeyboardButton(
        "ENVIAR", callback_data="finish")])

    update.callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(keyboard))

    return CHOOSING


def submit_selection(update, context):
    update.callback_query.answer()  # await for answer

    # Guarda as informacoes no BD
    # codigo aqui... (ta funfando por conta da lista ser passada por referencia)

    update.effective_message.reply_text('Seus interesses foram atualizados!')
    return ConversationHandler.END


# show => Mostra uma pessoa que tem interesses em comum (vai com base no ranking).
# Embaixo, um botão para enviar a solicitação de conexão deve existir.


def show(update, context):
    update.message.reply_text('Mostrei um amigo')
    return CHOOSE_ACTION

# random => Mostra uma pessoa aleatória. Embaixo, um botão para enviar a solicitação
# de conexão deve existir.


def random(update, context):
    update.message.reply_text('Random!!!')
    return CHOOSE_ACTION

# pending => Mostra todas as solicitações de conexão que aquela pessoa possui e
# para as quais ela ainda não deu uma resposta. Mostra, para cada solicitação,
# a descrição da pessoa e dois botões: conectar ou descartar).


def pending(update, context):
    update.message.reply_text('Mostrei os que faltam repsonde')
    return CHOOSE_ACTION

# friends => Mostra o contato (@ do Tele) de todas as pessoas com que o usuário
# já se conectou.


def friends(update, context):
    update.message.reply_text('Mostrei suas conexoes')
    return CHOOSE_ACTION

# mensagem ou comando desconhecido


# def unknown(update, context):
#     response_message = "Não entendi! Por favor, use um comando (eles começam com '/')."
#     update.message.reply_text(response_message)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    prefs_handler = ConversationHandler(
        entry_points=[CommandHandler('prefs', prefs)],

        states={
            CHOOSING: [CallbackQueryHandler(mark_category, pattern='^[\\d]+$'), CallbackQueryHandler(submit_selection, pattern='^finish$')],
        },

        fallbacks=[MessageHandler(Filters.text, submit_selection)],

        map_to_parent={
            ConversationHandler.END: CHOOSE_ACTION
        }
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REGISTER_NAME: [MessageHandler(Filters.text,
                                           register_name)],

            REGISTER_BIO: [MessageHandler(Filters.text,
                                          register_bio)],

            CHOOSE_ACTION: [
                prefs_handler,
                CommandHandler('show', show),
                CommandHandler('pending', pending),
                CommandHandler('friends', friends),
                CommandHandler('help', help),
            ],
        },

        fallbacks=[CommandHandler('start', start)]
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()
    logging.info("=== Bot running! ===")
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    logging.info("=== Bot shutting down! ===")


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
