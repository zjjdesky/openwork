import json
import random
import string
from datetime import datetime, timedelta

# Lists for generating realistic gaming data
ADJECTIVES = ["Shadow", "Dark", "Cyber", "Neon", "Toxic", "Epic", "Legendary", "Swift", "Silent", "Deadly", 
              "Mystic", "Frozen", "Blazing", "Storm", "Thunder", "Iron", "Steel", "Crystal", "Void", "Chaos",
              "Alpha", "Omega", "Prime", "Ultra", "Hyper", "Mega", "Super", "Quantum", "Cosmic", "Astral",
              "Savage", "Brutal", "Fierce", "Wild", "Rogue", "Ghost", "Phantom", "Stealth", "Ninja", "Samurai"]

NOUNS = ["Wolf", "Dragon", "Phoenix", "Hawk", "Tiger", "Viper", "Cobra", "Panther", "Falcon", "Raven",
         "Knight", "Warrior", "Hunter", "Slayer", "Sniper", "Assassin", "Ninja", "Samurai", "Gladiator", "Spartan",
         "Gamer", "Player", "Master", "Lord", "King", "Queen", "Prince", "Champion", "Legend", "Hero",
         "Wizard", "Mage", "Sorcerer", "Demon", "Angel", "Reaper", "Titan", "Giant", "Beast", "Monster"]

CLAN_NAMES = ["Elite Squad", "Dark Legion", "Phoenix Rising", "Shadow Warriors", "Cyber Knights",
              "Neon Ninjas", "Thunder Gods", "Ice Dragons", "Fire Hawks", "Storm Riders",
              "Void Walkers", "Chaos Syndicate", "Alpha Pack", "Omega Force", "Prime Division",
              "Quantum Collective", "Astral Guardians", "Savage Beasts", "Ghost Protocol", "Stealth Ops",
              "Night Stalkers", "Day Breakers", "Moon Runners", "Sun Chasers", "Star Lords",
              "Diamond Dogs", "Golden Eagles", "Silver Wolves", "Bronze Bulls", "Platinum Panthers",
              "Crimson Tide", "Azure Knights", "Emerald Empire", "Obsidian Order", "Jade Dragons",
              None, None, None, None, None]  # Some users not in clans

ACHIEVEMENTS = [
    "First Blood", "Double Kill", "Triple Kill", "Quad Kill", "Pentakill",
    "Unstoppable", "Godlike", "Legendary", "Dominating", "Rampage",
    "Sharpshooter", "Headhunter", "Sniper Elite", "Quick Draw", "Dead Eye",
    "Survivor", "Last One Standing", "Victory Royale", "Champion", "Undefeated",
    "Speed Demon", "Marathon Runner", "Night Owl", "Early Bird", "Dedicated",
    "Collector", "Completionist", "Explorer", "Adventurer", "Pioneer",
    "Team Player", "MVP", "Clutch Master", "Support Hero", "Tank Commander",
    "First Win", "10 Wins", "50 Wins", "100 Wins", "500 Wins",
    "Level 10", "Level 25", "Level 50", "Level 100", "Max Level",
    "Social Butterfly", "Lone Wolf", "Clan Leader", "Veteran", "Newcomer",
    "Premium Member", "Beta Tester", "Alpha Tester", "Founder", "VIP",
    "Holiday Hero 2023", "Summer Slayer", "Winter Warrior", "Spring Striker", "Fall Fighter"
]

RANKS = ["Bronze I", "Bronze II", "Bronze III", "Bronze IV",
         "Silver I", "Silver II", "Silver III", "Silver IV",
         "Gold I", "Gold II", "Gold III", "Gold IV",
         "Platinum I", "Platinum II", "Platinum III", "Platinum IV",
         "Diamond I", "Diamond II", "Diamond III", "Diamond IV",
         "Master", "Grandmaster", "Challenger", "Legend", "Immortal"]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "protonmail.com",
                 "icloud.com", "aol.com", "mail.com", "zoho.com", "fastmail.com"]

def generate_gamertag():
    style = random.choice(['adj_noun', 'adj_noun_num', 'word_num', 'xxx_style', 'name_style'])
    
    if style == 'adj_noun':
        return f"{random.choice(ADJECTIVES)}{random.choice(NOUNS)}"
    elif style == 'adj_noun_num':
        return f"{random.choice(ADJECTIVES)}{random.choice(NOUNS)}{random.randint(1, 9999)}"
    elif style == 'word_num':
        return f"{random.choice(NOUNS)}{random.randint(1, 9999)}"
    elif style == 'xxx_style':
        sep = random.choice(['_', 'x', 'X', '-', ''])
        return f"x{sep}{random.choice(NOUNS)}{sep}x{random.randint(1, 99)}"
    else:
        first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery", 
                       "Max", "Sam", "Charlie", "Jamie", "Drew", "Blake", "Skyler", "Dakota"]
        return f"{random.choice(first_names)}{random.choice(['_', '', 'x', 'X'])}{random.choice(NOUNS)}{random.randint(1, 999)}"

def generate_email(gamertag):
    clean_tag = ''.join(c.lower() for c in gamertag if c.isalnum())
    variation = random.choice([
        clean_tag,
        f"{clean_tag}{random.randint(1, 999)}",
        f"{clean_tag}_{random.randint(1, 99)}",
        f"gaming_{clean_tag}",
        f"{clean_tag}_gaming"
    ])
    return f"{variation}@{random.choice(EMAIL_DOMAINS)}"

def generate_user(user_id):
    gamertag = generate_gamertag()
    
    # Generate correlated stats
    level = random.randint(1, 100)
    xp = level * random.randint(800, 1200) + random.randint(0, 999)
    
    games_played = random.randint(10, 5000)
    
    # Win rate varies by skill level (higher levels tend to have better win rates)
    base_win_rate = 0.3 + (level / 100) * 0.3 + random.uniform(-0.15, 0.15)
    base_win_rate = max(0.1, min(0.9, base_win_rate))
    
    wins = int(games_played * base_win_rate)
    losses = games_played - wins
    
    # Rank correlates with level
    rank_index = min(len(RANKS) - 1, int((level / 100) * len(RANKS) * 0.8) + random.randint(-3, 3))
    rank_index = max(0, min(len(RANKS) - 1, rank_index))
    
    # Achievements based on level and games played
    num_achievements = min(len(ACHIEVEMENTS), random.randint(1, 5) + level // 10 + games_played // 500)
    achievements = random.sample(ACHIEVEMENTS, num_achievements)
    
    # Friends count
    friends_count = random.randint(0, 500)
    
    # Account dates
    days_since_created = random.randint(1, 2000)
    account_created = datetime.now() - timedelta(days=days_since_created)
    
    days_since_online = random.choices(
        [0, random.randint(1, 7), random.randint(8, 30), random.randint(31, 365)],
        weights=[0.4, 0.3, 0.2, 0.1]
    )[0]
    last_online = datetime.now() - timedelta(days=days_since_online, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    
    # Playtime correlates with games played and account age
    avg_game_length = random.uniform(0.2, 1.5)  # hours per game
    total_playtime_hours = round(games_played * avg_game_length + random.uniform(-50, 200), 1)
    total_playtime_hours = max(1, total_playtime_hours)
    
    # Premium status
    premium_subscriber = random.random() < 0.25  # 25% are premium
    
    return {
        "id": user_id,
        "gamertag": gamertag,
        "email": generate_email(gamertag),
        "level": level,
        "xp": xp,
        "rank": RANKS[rank_index],
        "games_played": games_played,
        "wins": wins,
        "losses": losses,
        "achievements": achievements,
        "friends_count": friends_count,
        "clan_name": random.choice(CLAN_NAMES),
        "account_created": account_created.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_online": last_online.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "premium_subscriber": premium_subscriber,
        "total_playtime_hours": total_playtime_hours
    }

def main():
    num_users = 1050
    users = [generate_user(i + 1) for i in range(num_users)]
    
    with open('/Users/hunter/Projects/github/langchain-ai/openwork/test_data/users_9.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"Generated {num_users} users successfully!")

if __name__ == "__main__":
    main()
