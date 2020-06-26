import sqlite3
db = sqlite3.connect('HR_bot.db')
cr = db.cursor()
cr.execute("""CREATE TABLE applicants_data(
                Name text,
                Mail_id text,
                Prefd_Jobrole text,
                Exp_pts integer,
                Skills_pts integer,
                Projects_pts integer,
                Total_pts integer
                )""")
    
db.commit()
db.close()

