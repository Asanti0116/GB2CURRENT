import sqlite3, os,sys

class DatabaseHandler():

    def __init__(self,url=""):
        self.url=url

    def __del__(self):
        if hasattr(self,'db'):
            try:
                self.db.close()
            except:
                pass

    def connectToDb(self):
        try:
            self.db=sqlite3.connect(self.url)	
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"[*] Error [*]\nType : {exc_type}\n Filename : {fname}\n Line : {exc_tb.tb_lineno}\nNote : DatabaseHandler->executeQueries : Database url is wrong.")
    def getLastPushId(self):
          return self.curs.lastrowid

    def executeQueries(self,queries=""):
        try:
            self.connectToDb()
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"[*] Erreur [*]\nType : {exc_type}\n Nom du Fichier : {fname}\n Ligne : {exc_tb.tb_lineno}\nNote : DatabaseHandler->executeQueries : Database url wrong.")
        self.curs=self.db.cursor()
        self.curs.execute(queries)
        try:
            return self.curs.fetchall()
        except:
            pass

    def commitChanges(self):
        try:
            self.db.commit()
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"[*] Erreur [*]\nType : {exc_type}\n Nom du Fichier : {fname}\n Ligne : {exc_tb.tb_lineno}\nNote : DatabaseHandler->commitChanges : Can't commit.")
    def closeDb(self):
        self.db.close()