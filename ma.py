import json
import random
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import logging
from data import get_profile, save_db
from deco import require_start
from about import show_profile, button
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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
    7495042500,
    7168610529,
    6621423491,
    1101488645,
    1661129466,
    5426641464,
    7153048444,
    5970118782
]




def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    profile = get_profile(user_id)

    if update.message.chat.type != 'private':
        update.message.reply_text("use this command in a private chat (DM).")
    else:
        if profile.get("start", False):
            update.message.reply_text("You have already started the bot.")
        else:
            profile["start"] = True
            save_db()

            update.message.reply_text(
                
                text=f"Hey {user.full_name} 🌀\nThis bot is made to manage ordinal legacy tours !" )

# Initialize the teams globally, so the HP changes are persistent within the bot's lifetime
teams = [
    {"name": "Phoenix1", "current_hp": 2000, "total_hp": 2000},
    {"name": "Phoenix2", "current_hp": 2000, "total_hp": 2000},
    {"name": "Cultured_Ones1", "current_hp": 2000, "total_hp": 2000},
    {"name": "Cultured_Ones2", "current_hp": 2000, "total_hp": 2000},
    {"name": "Infinityabyss1", "current_hp": 2000, "total_hp": 2000},
    {"name": "Infinityabyss2", "current_hp": 2000, "total_hp": 2000},
    {"name": "UndefinedRepublic1", "current_hp": 2000, "total_hp": 2000},
    {"name": "UndefinedRepublic2", "current_hp": 2000, "total_hp": 2000},
    {"name": "InvincibleCult1", "current_hp": 2000, "total_hp": 2000},
    {"name": "InvincibleCult2", "current_hp": 2000, "total_hp": 2000},
]

@require_start
def show_teams(update: Update, context: CallbackContext):
    
    if update.message.from_user.id not in members:
            update.message.reply_text("You don't have permission to use this command.")
            return
            
    result = "Teams:\n\n"

    for idx, team in enumerate(teams, start=1):
        # Create the HP bar based on current and total HP
        hp_bar = create_hp_bar(team['current_hp'], team['total_hp'])
        result += f"Team: {team['name'].title()} ({idx})\n"
        result += f"HP: {team['current_hp']}/{team['total_hp']}\n"
        result += f"{hp_bar}\n\n"

    update.message.reply_text(result)



# List of teams

import random
import time

# Define guilds
guilds = {
    "Phoenix": ["Phoenix1", "Phoenix2"],
    "Cultured_Ones": ["Cultured_Ones1", "Cultured_Ones2"],
    "Infinityabyss": ["Infinityabyss1", "Infinityabyss2"],
    "Undefinedrepublic": ["Undefinedrepublic1", "Undefinedrepublic2"],
    "Invinciblecult": ["Invinciblecult1", "Invinciblecult2"]
}

# Flatten the list of teams from guilds
teamm = [team for sublist in guilds.values() for team in sublist]

def random_matchups(update: Update, context: CallbackContext) -> None:
    # Check if the user is an owner
    if update.message.from_user.id not in owner_ids:
        update.message.reply_text("You don't have permission to use this command.")
        return

    # Shuffle the teams randomly
    random.shuffle(teamm)

    # Create matchups avoiding teams from the same guild
    matchups = []
    used_teamm = set()

    def find_opponent(team):
        for opponent in teamm:
            # Check if the opponent is not used and not in the same guild
            if opponent not in used_teamm and not any(opponent in guilds[g] for g in guilds if team in guilds[g]):
                return opponent
        return None

    for team in teamm:
        if team in used_teamm:
            continue
        opponent = find_opponent(team)
        if opponent:
            matchups.append((team, opponent))
            used_teamm.add(team)
            used_teamm.add(opponent)
        # Ensure that only 5 matchups are made (since there are 10 teams and 5 matches)
        if len(matchups) == len(teamm) // 2:
            break

    # Prepare animation sequence
    animations = [
        "🔵      🔴",
        "🔴    🔵",
        " 🔵  🔴",
        "    🟣   "
    ]

    # Send the first message that will be edited during the animation
    sent_message = update.message.reply_text(animations[0])

    # Edit the message step by step with a short delay for animation
    for frame in animations[1:]:
        time.sleep(0.5)  # Wait for 0.5 seconds before updating the next frame
        sent_message.edit_text(frame)

    # After the animation, prepare the final matchups message
    message = "Matchups:\n\n"
    for match_number, (team1, team2) in enumerate(matchups, 1):
        message += f"Match {match_number}: {team1} vs {team2}\n\n"

    # Edit the message one last time to display the matchups
    sent_message.edit_text(message)

def create_hp_bar(current_hp, total_hp, bar_length=20):
    # Create a visual HP bar
    filled_length = int(bar_length * current_hp // total_hp)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    return f"{bar}"    

  # List of members who have permission to use these commands

@require_start
def shopping(update: Update, context: CallbackContext):
    
    # Check if the user has permission
    if update.message.from_user.id not in members:
        update.message.reply_text("You don't have permission to use this command.")
        return

    # Hardcoded list of champions and their prices
    champions = {
        "Leoxi": 100,
        "Roland zain": 100,
        "Jessie": 100,
        "Henry Damian": 100,
        "Triton": 100,
        "Djino": 100,
        "Kragthar": 100,
        "Mayla": 100,
        "Thadues": 100,
        "Ophikira": 100,
        "Kayla": 100,
        "Ghatokaca": 100,
        "Gladranox": 100,
        "Vereena": 100,
        "Hanzo": 100  # Keep Hanzo's count as it is
    }

    shop_message = "Available Champions for Sale:\n\n"
    for champion, price in champions.items():
        shop_message += f"- {champion.title()}: {price} coins\n"

    update.message.reply_text(shop_message)
    
    
@require_start  
def buy(update: Update, context: CallbackContext):

    # Check if the user has permission
    if update.message.from_user.id not in members:
        update.message.reply_text("You don't have permission to use this command.")
        return

    user_id = update.effective_user.id
    if not context.args:
        update.message.reply_text("Please specify a champion to buy.")
        return
    
    # Convert user input to lowercase
    champion_name = context.args[0].lower()
    profile = get_profile(user_id)

    # Hardcoded list of champions with names converted to lowercase
    champions = {
        "leoxi": 100,
        "roland zain": 100,
        "jessie": 100,
        "henry damian": 100,
        "triton": 100,
        "djino": 100,
        "kragthar": 100,
        "mayla": 100,
        "thadues": 100,
        "ophikira": 100,
        "kayla": 100,
        "ghatokaca": 100,
        "gladranox": 100,
        "vereena": 100,
        "hanzo": 100  # Keep Hanzo's count as it is
    }

    # Check if the champion is available
    champion_price = champions.get(champion_name)

    if champion_price is None:
        update.message.reply_text("This champion is not available.")
        return
    
    if champion_name in profile.get('champions', {}):
        update.message.reply_text("You already own this champion.")
        return

    if profile['coins'] < champion_price:
        update.message.reply_text("You don't have enough coins.")
        return
    
    # Deduct coins and add champion to profile
    profile['coins'] -= champion_price
    if 'champions' not in profile:
        profile['champions'] = {}
    profile['champions'][champion_name] = profile['champions'].get(champion_name, 0) + 1
    save_db()

    update.message.reply_text(f"You have successfully bought {champion_name.title()}!")


owner_ids = [6440036107, 6430590480]  # List of owner IDs

@require_start    
def add(update: Update, context: CallbackContext) -> None:
    
    if update.message.reply_to_message:
        target_user_id = update.message.reply_to_message.from_user.id
        
        # Check if the user executing the command is an owner
        if update.message.from_user.id not in owner_ids:
            update.message.reply_text("You don't have permission to use this command.")
            return
        
        if len(context.args) != 1:
            update.message.reply_text("Please provide the amount of coins to add, e.g., /add 500")
            return
        
        try:
            coins_to_add = int(context.args[0])
        except ValueError:
            update.message.reply_text("Invalid coins amount. Please provide a valid number.")
            return

        # Fetch the target user's profile
        profile = get_profile(target_user_id)
        
        # Add the coins to the user's profile
        profile['coins'] += coins_to_add

        # Save the updated profile back to the database
        save_db()

        # Notify the admin that the coins were added successfully
        update.message.reply_text(f"Added {coins_to_add} coins to {update.message.reply_to_message.from_user.first_name}'s profile.")
    
    else:
        update.message.reply_text("Please reply to a user's message to add coins to their profile.")                                                                                                      
def main():
    updater = Updater("7127475745:AAEg48FiQBmmw5zJAkj9ZEwL_mpeb0mWN3s")
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start)) 
  
  
    dispatcher.add_handler(CommandHandler('showteams', show_teams)) 
 
    dispatcher.add_handler(CallbackQueryHandler(button, pattern='^profile_'))
    dispatcher.add_handler(CommandHandler('about', show_profile)) 
    dispatcher.add_handler(CommandHandler('shopping', shopping))
    dispatcher.add_handler(CommandHandler('buy', buy)) 
    dispatcher.add_handler(CommandHandler('add', add)) 
    dispatcher.add_handler(CommandHandler('shuffle', random_matchups)) 
    
    
    

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()