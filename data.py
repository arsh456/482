import json
# Initialize the database dictionary
db = {
    "profiles": {},  # User-specific profiles
    "participants": [],  # Global list of participants
    "teams": [],
    "shop": {}  # Global list of teams
}

# Load the database from the JSON file
try:
    with open("database.json", "r") as file:
        db = json.load(file)
except FileNotFoundError:
    db = {"profiles": {}, "participants": [], "teams": [], "shop": {}}

# Save the database to the JSON file
def save_db():
    with open("database.json", "w") as file:
        json.dump(db, file, indent=4)
        

def get_profile(user_id):
    user_id_str = str(user_id)

    # Default profile structure
    default_profile = {
        "start": False,
        "coins": 2000,
        "champions": {}
    }

    # If user profile doesn't exist, create it
    if user_id_str not in db["profiles"]:
        db["profiles"][user_id_str] = default_profile
        save_db()
    else:
        profile = db["profiles"][user_id_str]
        # Ensure all default fields are present
        for key, value in default_profile.items():
            if key not in profile:
                profile[key] = value
        save_db()

    # Return the user's profile
    return db["profiles"][user_id_str]