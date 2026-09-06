import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
from groq import Groq

app = Flask(__name__, static_folder='.')

# Connect to Groq using the FREE key environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def scrape_forum():
    # MAXIMIZED COMPREHENSIVE LIVE RUSSIA MASTER ENCYCLOPEDIA DATA SYSTEM
    ultimate_master_database = """
    ========================================================================
    CHAPTER 1: CHAT & BASIC ROLEPLAY TERMINOLOGY / ACTIONS
    ========================================================================
    - IC (In Character) Chat: Strictly for in-game life conversation. No real-life topics.
    - OOC (Out Of Character) Chat: For real-life talk. Done via commands: /n, /b, /fn (family OOC), /rb (faction OOC).
    - DM (Deathmatch): Hurting, shooting, or killing any player without a valid, approved RP reason.
    - DB (DriveBy): Killing/damaging players using a vehicle or driving over them intentionally.
    - SK (Spawn Kill): Attacking/killing players at their exact spawn entry, login point, or base interior exit.
    - RK (Revenge Kill): Dying, respawning at the hospital, and returning to kill the person who beat you.
    - PG (Powergaming): Unrealistic superhuman gameplay (e.g., jumping from bridges without damage, fighting a whole squad alone).
    - MG (Metagaming): Grabbing information from real life (like discord or player names over their heads) and using it inside IC gameplay.
    - TK (Team Kill): Damaging or killing players who are inside your own faction or sub-unit squad.
    - BH (Bunnyhopping): Non-stop jumping while sprinting to move faster.
    - FR (Fast Reload): Glitching animation setups to reload firearms faster than normal.
    - GZ (Green Zone): Safety zones where zero fighting is tolerated (Hospital, Spawn houses, Jobs, Shops, Gov bases).

    ========================================================================
    CHAPTER 2: PROJECT SERVER LAWS & OFFICIAL PUNISHMENTS
    ========================================================================
    - Rule 1.01: Green Zone Fighting - Assaulting anyone inside peaceful public structures.
      * Punishment: Jail (Demorgan) for 60-120 minutes or a Warning account marker (Warn).
    - Rule 1.02: DM / Deathmatch - Unjustified violent attacks or execution of players.
      * Punishment: Jail (Demorgan) for 30-120 minutes.
    - Rule 1.03: DB / DriveBy - Vehicular homicide or hit-and-run tactics.
      * Punishment: Jail (Demorgan) for 30-90 minutes.
    - Rule 1.04: MG / Metagaming - Infusing OOC topics into local IC dialogue streams.
      * Punishment: Chat Mute (Мут) for 10-30 minutes.
    - Rule 1.05: PG / Powergaming - Acting out non-human properties or fantasy capabilities.
      * Punishment: Jail (Demorgan) for 30-60 minutes or a Warning (Warn).
    - Rule 1.06: SK / Spawn Kill - Targeting players immediately upon initial login/spawn states.
      * Punishment: Jail for 60-120 minutes or an active Warning (Warn).
    - Rule 1.07: TK / Team Kill - Killing associates inside your own organization team.
      * Punishment: Faction Blacklist Kick or a Warning account badge (Warn).
    - Rule 1.08: RK / Revenge Kill - Seeking immediate combat retaliation post-hospital revival.
      * Punishment: Jail (Demorgan) for 30-60 minutes.
    - Rule 1.09: Cheating & Third-Party Software - Utilizing hacks, scripts, aimbots, cleo file injectors, auto-clickers, or external memory mod programs.
      * Punishment: PERMANENT ACCOUNT BAN across all server databases.
    - Rule 1.10: Financial Scams & Fraud - Tricking players during trading deals for virtual currency, vehicles, or properties.
      * Punishment: PERMANENT ACCOUNT BAN accompanied by a full character database asset wipe.
    - Rule 1.11: Staff Harassment & Admin Insults - Disrespecting, defaming, or insulting game guides, server assistants, or core developers.
      * Punishment: Text channel mute for 60-300 minutes or a Temporary Account Ban for 1-7 days.
    - Rule 1.12: Unauthorized Advertising - Spreading external internet links, concurrent servers, or discord invite chains.
      * Punishment: Permanent Account Ban.
    - Rule 1.13: Non-RP Behaviour - Actions breaking core structural physics (e.g., logging out during active arrests, shooting while healing).
      * Punishment: Jail (Demorgan) for 30-60 minutes.

    ========================================================================
    CHAPTER 3: CRITICAL WARN RESTRICTION LAWS (ВАРНЫ)
    ========================================================================
    If an admin issues an active account warning (Warn), the system locks down these systems automatically:
    1. BANNED from purchasing any weapon from ammunition stores or retrieving inventory from family vaults.
    2. BANNED from initializing trades at the Central Market or executing property deeds (Houses, Businesses, Cars).
    3. BANNED from entering any official government or criminal faction structure.
    4. BANNED from leasing plot zones or starting operations inside private greenhouses.

    ========================================================================
    CHAPTER 4: OFFICIAL FORUM RULES & WEB REGULATIONS
    ========================================================================
    - Forum Rule 2.01: Flood & Thread Spamming - Posting multi-form duplication tickets or endless useless content.
      * Punishment: 1-3 days Forum Profile Suspension and immediate web data deletion.
    - Forum Rule 2.02: Multi-Accounting Exploitation - Launching secondary alternative forum accounts to evade active moderation blocks.
      * Punishment: Permanent profile ban for all auxiliary web identities.
    - Forum Rule 2.03: Inappropriate Profiles - Setting adult media backgrounds, slurs, explicit terms, or hateful logos as avatars/tags.
      * Punishment: Total page locking until modified and reviewed by server managers.
    - Forum Rule 2.04: Toxic Flame wars - Instigating toxic drama inside player complaint files or leadership boards.
      * Punishment: Complete forum account block ranging from 3 to 14 days.

    ========================================================================
    CHAPTER 5: COMMAND SYSTEM & GPS MAP DIRECTORY (/gps)
    ========================================================================
    - Main Menu Interface: Type /gps to display navigation tracks.
    - Public Church / Vatican Cathedral Location: /gps -> Public Places (Важные места) -> Arzamas Church (Церковь г. Арзамас).
    - Public Mosque Location: /gps -> Public Places (Важные места) -> Mosque (Мечеть).
    - Government Headquarters Base: /gps -> State Organizations -> Government (Правительство).
    - FSB Base Station: /gps -> State Organizations -> Federal Security Service (ФСБ).
    - Main Traffic Police Outpost: /gps -> State Organizations -> GIBDD (г. Южный).
    - Urban Police Department Base: /gps -> State Organizations -> UMVD (г. Арзамас).
    - Military Army Barracks Location: /gps -> State Organizations -> Army (Воинская часть).
    - Central Auto Market Hub: /gps -> Public Places -> Car Market.

    ========================================================================
    CHAPTER 6: JOBS, ECONOMY, & FACTION LEADERSHIP
    ========================================================================
    - Job Types: Trucker (Дальнобойщики), Firefighter (Пожарные), Garbage Collector, Farmer (Фермер).
    - Greenhouses (Теплицы): Must purchase a private house property first, navigate to the Garden Store, purchase a structural construction layout blueprint, and execute build modes. Entering promo code '#farm' applies bonus cash modifiers.
    - Support Agents Section: Main Forum -> Server Directory -> Help/Complaints -> Support Agent Board. Handles player questions via the in-game help text commands /h or /helpme.
    - Faction Leadership Selection: Open application topics are posted inside the server-specific board labeled 'Заявления на пост лидера'. Candidates must submit age, game hours, and clean records.
    """
    try:
        url = "https://forum.liverussia.online/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()[:1000] + "\n" + comprehensive_database
    except Exception as e:
        print(f"Scraper layer redirect active: {e}")
    return comprehensive_database

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    user_question = data.get('question', '')
    
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400
        
    forum_context = scrape_forum()
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are the absolute master AI guide for the LIVE RUSSIA mobile roleplay game forum. "
                        f"Answer all questions with total accuracy using this full comprehensive database: {forum_context}. "
                        f"STRICT COMPLIANCE MANDATES: "
                        f"1. You must write your responses entirely and completely in English only. "
                        f"2. Never print out any Russian text, Cyrillic letters, or words from the source files. Always translate them seamlessly into clean English strings. "
