import sqlite3


conn = sqlite3.connect('movie.db')
cursor = conn.cursor()
cursor.execute('select * from movie where get=0')

conn = sqlite3.connect('movie.db')
cursor = conn.cursor()
cursor.execute('select * from movie where get=0')
links = [x[0] for x in cursor.fetchall()]
cursor.close()
conn.close()
print('get=0:', links)



#url = cursor.fetchall()[0][0]
#print(url)
#cursor.execute('insert into dlinks (title, title2, p_link, d_link, pwd) values (?, ?, ?, ?, ?)', ('魔力麦克 Magic Mike (2012)', '', url, 'https://pan.baidu.com/s/1o6sXvHg', ''))
#cursor.execute('update movie set get=1 where p_link=?', (url,))
#cursor.close()
#conn.commit()
#conn.close()
#print('Done.')
