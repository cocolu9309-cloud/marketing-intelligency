import sqlite3
conn = sqlite3.connect('data/products.db')
c = conn.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE type='table'")
print('Table schema:', c.fetchone()[0])
c.execute("SELECT sql FROM sqlite_master WHERE type='index'")
print('Indexes:', [r[0] for r in c.fetchall()])
conn.close()
print("Verification complete.")