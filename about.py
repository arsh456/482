import json
import random
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import logging
from data import get_profile, save_db
from deco import require_start


members = [ 
    6440036107,
    6430590480,
    163494588,
    6495101094,
    6230265985,
    6554200916,
    6675283297,
    5784943235,
    1368587746,
    2059829797,
    6935772501,
    5153974036,
    1444258617,
    1222612909,
    1615360672,
    1496817722,
    6716962045,
    1291904139,
    1786637879,
    1001774029,
    986380678,
    6740610657,
    7182184531,
    7033418582,
    1018958549,
    6344210538,
    5909849185,
    1507821455,
    6061178519,
    1508086602,
    5443647765,
    1856430691,
    1257427765,
    1227758573,
    6614617069,
    7165876444,
    7168610529,
    6621423491,
    1101488645,
    1661129466,
    5426641464,
    7153048444,
    5970118782,
    1291904139,
    5426641464,
    7153048444
]







profile_tracking = {}

@require_start
def show_profile(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Check if the user is in the 'members' list
    if user_id not in members:
        update.message.reply_text("You don't have permission to use this command.")
        return

    user_name = update.effective_user.first_name
    profile = get_profile(user_id)

    profile_message = (
        f" 「Profile」:\n\n"
        f"-🆔 UserID: {user_id}\n"
        f"-👤 User Name: {user_name}\n\n"
        f"「Resource Info」:\n\n"
        f"-🪙 Coins : {profile['coins']}\n"
    )

    keyboard = [
        [InlineKeyboardButton("Champions", callback_data='profile_view_items')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:  # For regular text message updates
        message = update.message.reply_text(profile_message, reply_markup=reply_markup)
        profile_tracking[message.message_id] = user_id
    elif update.callback_query:  # For callback query updates (button clicks)
        query = update.callback_query
        query.edit_message_text(text=profile_message, reply_markup=reply_markup)
        profile_tracking[query.message.message_id] = user_id


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    # Check if the user is in the 'members' list
    if user_id not in members:
        query.answer("You don't have permission to use this.")
        return

    if query.message.message_id in profile_tracking:
        if user_id != profile_tracking[query.message.message_id]:
            query.answer("This is not your profile.")
            return

        profile = get_profile(user_id)

        if query.data == 'profile_view_items':
            champions = profile.get('champions', {}).keys()  # Only get the champion names, not counts
            full_name = profile.get('full_name', "Unknown User")
            if champions:
                items_message = f"Champions Owned By {full_name}:\n\n" + "\n".join([f"- {champion.title()}" for champion in champions])
            else:
                items_message = "You have no champions."

            keyboard = [
                [InlineKeyboardButton("Main", callback_data='profile_main')],
            ]

            query.edit_message_text(text=items_message, reply_markup=InlineKeyboardMarkup(keyboard))

        elif query.data == 'profile_main':
            # Go back to main profile
            show_profile(update, context)

        else:
            query.answer("Unknown action.")
    else:
        query.answer("Invalid request.")