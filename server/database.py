import mysql.connector

DB_INFORMATIONS = {
    'user'      : 'root',
    'password'  : '',
    'host'      : '127.0.0.1',
    'database'  : 'multitron'
}

class Database:
    db = None

    @staticmethod
    def connect():
        Database.db = mysql.connector.connect(**DB_INFORMATIONS)

    @staticmethod
    def insert_client(username, password):
        # Pseudo already exists ?
        cursor = Database.db.cursor()
        query = 'SELECT * FROM player WHERE login = %s'
        cursor.execute(query, [username])
        result = cursor.fetchone()
        
        if result:
            return False
        
        cursor.close()
        
        cursor = Database.db.cursor()
        query = 'INSERT INTO player (login, password, score, isAdmin) VALUES (%s, %s, 0, 0)'
        cursor.execute(query, [username, password])
        Database.db.commit()
        cursor.close()
        
        return True
        
    @staticmethod
    def check_client(username, password):
        cursor = Database.db.cursor()
        query = 'SELECT * FROM player WHERE login = %s AND password = %s'
        cursor.execute(query, [username, password])
        result = cursor.fetchone()

        cursor.close()

        if result:
            return True
        else:
            return False

    @staticmethod
    def get_all_scores():
        cursor = Database.db.cursor()
        query = 'SELECT login, score FROM player ORDER BY score DESC'
        cursor.execute(query)

        scores = []
        for (login, score) in cursor:
            scores.append([login, score])

        cursor.close()

        return scores

    @staticmethod
    def update_scores(username, score):
        cursor = Database.db.cursor()
        query = 'UPDATE player SET score = score + ' + str(score) + ' WHERE login = "' + str(username) + '"'
        cursor.execute(query, [])
        Database.db.commit()
        cursor.close()