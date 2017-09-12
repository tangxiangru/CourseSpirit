# coding=utf-8
from flask import Flask, request
import base64, hashlib, psycopg2
import

#app = Flask(__name__)

#返回ans：
#     -1：没有此用户
#	   0：成功登陆
#	   1：密码错误
@app.route('/login/', methods=['GET'])
def login():
    ans = '';
        if request.method == 'GET':
            username = request.args.get('username')							#获取用户名
                password = request.args.get('password')							#获取base64加密后的密码
                
                password = decode_secret = base64.b64decode(password)			#base64解密
                
                #链接数据库
                conn = psycopg2.connect(database="ktjl", user="postgres", password="admin", host="127.0.0.1", port="5432")
                cur = conn.cursor()
                
                #获取用户id
                cur.execute("SELECT id FROM public.users WHERE username = '%s';" % (username,))
                conn.commit()
                rows = cur.fetchall()        # all rows in table
                if len(rows) == 0:											#没有此用户
                    ans = '-1'
                else:
                    uid = rows[0][0]
                        #获取该用户盐值
                        cur.execute("SELECT salt FROM public.salt WHERE uid = '%s';" % (uid,))
                        conn.commit()
                        rows = cur.fetchall()        # all rows in table
                        salt = rows[0][0]
                        password = md5(md5(password) + salt)
                        
                        #获取数据库中加密后的密码
                        cur.execute("SELECT password FROM public.users WHERE id = '%s';" % (uid,)) 
                        conn.commit()
                        rows = cur.fetchall()        # all rows in table
                        dbpassword = rows[0][0]
                        
                        if dbpassword == password :
                            ans = '0'
                        else:
                            ans = '1'
        return ans

def md5(str):
    m = hashlib.md5()
        m.update(str)
        return m.hexdigest()


#if __name__ == '__main__':
#	app.run(debug=True)	
