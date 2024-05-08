import sqlite3


class ScoreboardDB:
    def __init__(self, db_path='scoreboard.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS scores
                     (user_id TEXT PRIMARY KEY, score INTEGER)''')
        conn.commit()
        conn.close()

    def increment_score(self, user_id, increment=1):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT score FROM scores WHERE user_id = ?', (user_id,))
        result = c.fetchone()

        if result:
            new_score = result[0] + increment
            c.execute('UPDATE scores SET score = ? WHERE user_id = ?', (new_score, user_id))
        else:
            c.execute('INSERT INTO scores (user_id, score) VALUES (?, ?)', (user_id, increment))

        conn.commit()
        conn.close()

    def get_score(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT score FROM scores WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        conn.close()

        return result[0] if result else None

    def get_leaderboard(self, top_n=10):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT user_id, score FROM scores ORDER BY score DESC LIMIT ?', (top_n,))
        leaderboard = c.fetchall()
        conn.close()
        return leaderboard
