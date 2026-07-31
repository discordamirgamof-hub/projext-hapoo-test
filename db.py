import sqlite3
import time
from config import XP_PER_LEVEL

DB_NAME = "hapooie.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 100,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            fish INTEGER DEFAULT 0,
            dogs INTEGER DEFAULT 0,
            bank_balance INTEGER DEFAULT 0,
            prison_until INTEGER DEFAULT 0,
            prison_fine INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_bets (
            user_id INTEGER PRIMARY KEY,
            game_type TEXT,
            bet_amount INTEGER,
            prediction TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, points, level, xp, fish, dogs, bank_balance, prison_until, prison_fine FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cursor.execute("SELECT user_id, points, level, xp, fish, dogs, bank_balance, prison_until, prison_fine FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
    conn.close()
    return {
        "user_id": row[0],
        "points": row[1],
        "level": row[2],
        "xp": row[3],
        "fish": row[4],
        "dogs": row[5],
        "bank_balance": row[6],
        "prison_until": row[7],
        "prison_fine": row[8]
    }

def update_user(user_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    values = list(kwargs.values()) + [user_id]
    cursor.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
    conn.commit()
    conn.close()

def add_xp(user_id, amount=1):
    user = get_user(user_id)
    new_xp = user["xp"] + amount
    new_level = user["level"]
    if new_xp >= XP_PER_LEVEL:
        new_level += new_xp // XP_PER_LEVEL
        new_xp = new_xp % XP_PER_LEVEL
    update_user(user_id, xp=new_xp, level=new_level)

def set_pending_bet(user_id, game_type, bet_amount, prediction=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO pending_bets (user_id, game_type, bet_amount, prediction) VALUES (?, ?, ?, ?)",
        (user_id, game_type, bet_amount, prediction)
    )
    conn.commit()
    conn.close()

def get_pending_bet(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT game_type, bet_amount, prediction FROM pending_bets WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"game_type": row[0], "bet_amount": row[1], "prediction": row[2]}
    return None

def clear_pending_bet(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pending_bets WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()