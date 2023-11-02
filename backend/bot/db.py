import sqlite3
from datetime import datetime


def create_tables():
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        # For members
        c.execute('''CREATE TABLE IF NOT EXISTS members 
                     (name TEXT, nickname TEXT, role TEXT)''')
        # For storing guild name
        c.execute('''CREATE TABLE IF NOT EXISTS guild_info 
                     (key TEXT PRIMARY KEY, value TEXT)''')
        # For storing user warnings
        c.execute('''CREATE TABLE IF NOT EXISTS warns
                     (warn_id INTEGER PRIMARY KEY, user_id INTEGER, issuer_id INTEGER, reason TEXT, timestamp TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS punishments
                     (punishment_id INTEGER PRIMARY KEY, user_id INTEGER, issuer_id INTEGER, 
                      type TEXT, reason TEXT, timestamp TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS coins
                     (user_id INTEGER PRIMARY KEY, amount INTEGER)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS daily_usage
                     (user_id INTEGER PRIMARY KEY, last_used TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS levels
                     (user_id INTEGER PRIMARY KEY, xp INTEGER, level INTEGER)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS message_stats
                     (user_id INTEGER PRIMARY KEY, message_count INTEGER, last_message_time TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS events
                    (event_id INTEGER PRIMARY KEY, name TEXT, 
                    date_and_time TEXT, reward TEXT, timezone TEXT, role_id INTEGER)''')


        conn.commit()

# Update your add_event function
def add_event(name, date_and_time, reward, timezone, role_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO events (name, date_and_time, reward, timezone, role_id) VALUES (?, ?, ?, ?, ?)",
                  (name, date_and_time, reward, timezone, role_id))
        conn.commit()

def delete_event(name):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT role_id FROM events WHERE name = ?", (name,))
        role_id = c.fetchone()[0]
        c.execute("DELETE FROM events WHERE name = ?", (name,))
        conn.commit()
    return role_id


def get_events():
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM events")
        events = c.fetchall()
        return events
    
        
def get_message_count(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT message_count FROM message_stats WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0] if result else 0
     
def get_last_message_time(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT last_message_time FROM message_stats WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0] if result else None

def set_last_message_time(user_id, last_message_time):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO message_stats (user_id, message_count, last_message_time) VALUES (?, 0, ?)", (user_id, last_message_time))
        c.execute("UPDATE message_stats SET last_message_time = ? WHERE user_id = ?", (last_message_time, user_id))
        conn.commit()

def update_message_count(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO message_stats (user_id, message_count, last_message_time) VALUES (?, 0, '')", (user_id,))
        c.execute("UPDATE message_stats SET message_count = message_count + 1 WHERE user_id = ?", (user_id,))
        conn.commit()


def add_xp(user_id, xp):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO levels (user_id, xp, level) VALUES (?, 0, 1)", (user_id,))
        c.execute("UPDATE levels SET xp = xp + ? WHERE user_id = ?", (xp, user_id))
        conn.commit()
        
def get_level(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT level FROM levels WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0] if result else 0

def get_level_and_xp(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT level, xp FROM levels WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result if result else (1, 0)

def update_level(user_id, new_level, new_xp):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE levels SET level = ?, xp = ? WHERE user_id = ?", (new_level, new_xp, user_id))
        conn.commit() 
        
def set_daily_usage(user_id):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Store timestamp as UTC
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO daily_usage (user_id, last_used) VALUES (?, ?)", (user_id, timestamp))
        conn.commit()

def get_daily_usage(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT last_used FROM daily_usage WHERE user_id=?", (user_id,))
        result = c.fetchone()
        return result[0] if result else None
    
def update_members_db(members_data):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM members")  # Remove existing records
        c.executemany("INSERT INTO members (name, nickname, role) VALUES (?, ?, ?)", members_data)
        conn.commit()

def fetch_members():
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT name, nickname, role FROM members")
        return c.fetchall()
    
def update_guild_name(guild_name):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO guild_info (key, value) VALUES (?, ?)", ("guild_name", guild_name))
        conn.commit()

def fetch_guild_name():
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT value FROM guild_info WHERE key=?", ("guild_name",))
        result = c.fetchone()
        return result[0] if result else None
    
def add_warn(user_id, issuer_id, reason):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO warns (user_id, issuer_id, reason, timestamp) VALUES (?, ?, ?, ?)", 
                  (user_id, issuer_id, reason, timestamp))
        conn.commit()

def get_warns(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT warn_id, issuer_id, reason, timestamp FROM warns WHERE user_id=?", (user_id,))
        return c.fetchall()

def get_warn(warn_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, issuer_id, reason, timestamp FROM warns WHERE warn_id=?", (warn_id,))
        return c.fetchone()

def remove_warn(warn_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM warns WHERE warn_id=?", (warn_id,))
        conn.commit()
        
def add_punishment(user_id, issuer_id, type_, reason):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO punishments (user_id, issuer_id, type, reason, timestamp) VALUES (?, ?, ?, ?, ?)", 
                  (user_id, issuer_id, type_, reason, timestamp))
        conn.commit()

def get_punishments(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT punishment_id, issuer_id, type, reason, timestamp FROM punishments WHERE user_id=?", 
                  (user_id,))
        return c.fetchall()

def get_punishment(punishment_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, issuer_id, type, reason, timestamp FROM punishments WHERE punishment_id=?", 
                  (punishment_id,))
        return c.fetchone()

def remove_punishment(punishment_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM punishments WHERE punishment_id=?", (punishment_id,))
        conn.commit() 
        
def add_coins(user_id, amount):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO coins (user_id, amount) VALUES (?, 0)", (user_id,))  # ensure a record exists
        c.execute("UPDATE coins SET amount = amount + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def remove_coins(user_id, amount):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE coins SET amount = amount - ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def get_coins(user_id):
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT amount FROM coins WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0] if result else 0
    
def get_leaderboard():
    with sqlite3.connect('members.db') as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, amount FROM coins ORDER BY amount DESC")
        return c.fetchall()