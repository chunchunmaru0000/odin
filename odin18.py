import pymysql

connectScores = pymysql.connect(host='host', user='root', password='root', database='scores')

cur = connectScores.cursor()

cur.execute('select avg(math) from scores')
result = cur.fetchall()

connectScores.commit()
cur.close()
connectScores.close()

print(f'avg(math)\n{result}')