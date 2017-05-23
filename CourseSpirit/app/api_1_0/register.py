# coding=utf-8
from flask import Flask, request, jsonify
from .. import db
from . import api
from random import Random
import psycopg2, hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

host = '0.0.0.0'
port = '5000'

app = Flask(__name__)

#retuan ans(String)
#-1             用户名已经被注册
#0              注册成功

@app.route('/register', methods=['POST'])
def register():
    reload(sys)
    if request.method == 'POST':
        role = request.form.get('role').encode('utf-8')#身份
        #            role = role[1:len(role) - 2].encode('utf-8')
        
        email = request.form.get('email')                                           #邮箱
        #           email = email[1:len(email) - 2].encode('utf-8')
        
        username = request.form.get('username').encode('utf-8')                                     #用户名
        #           username = username[1:len(username) - 2].encode('utf-8')
        
        password = request.form.get('password')                                     #密码
        #            password = password[1:len(password) - 2].encode('utf-8')
        
        no = request.form.get('no')                                                         #学号/工号
        #            no = no[1:len(no) - 2]
        
        department = request.form.get('department').encode('utf-8')                         #院系
        #            department = department[1:len(department) - 2]
        grade_or_title = request.form.get('grade_or_title')         #年级或职称
        #            grade_or_title = grade_or_title[1:len(grade_or_title) - 2]
        
        salt = create_salt()                                                                               #盐值
        print 'salt = ', salt
        print 'password = ', password
        password = md5(md5(password) + salt)                                                #加盐加密
        print 'password = ', password
        
        print 'role = ', role
        print 'email= ', email
        print 'username = ', username
        print 'password = ', password
        print 'no = ', no
        print 'department = ', department
        print 'grade_or_title = ', grade_or_title
        
        
        
        conn = psycopg2.connect(database="ktjl", user="op", password="123456", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        
        ans = ""
        #查询该用户名是否存在
        sql = "SELECT id FROM public.users WHERE username = %s;" % (username,)
        print sql
        cur.execute("SELECT id FROM public.users WHERE username = '%s';" % (username,))
        conn.commit()
        rows = cur.fetchall()        # all rows in table
        if len(rows) == 0:
                  #没被注册
        #存储用户通用信息
                cur.execute('''INSERT INTO public.users (no, type, email, username, password)
                            VALUES (%s, %s, %s, %s, %s);''' , (no, role, email, username, password))
                    
                    
                    conn.commit()
                        #获取用户id
                    cur.execute("SELECT id FROM public.users WHERE username = %s;", (username,))
                    conn.commit()
                    uid = cur.fetchall()[0][0]
                                    
                                    #存储盐值
                    cur.execute('''INSERT INTO public.salt (uid, salt) VALUES (%s, %s);''', (uid, salt))
                    conn.commit()
                                            
                                            
                    cur.execute('''INSERT INTO public.user_info (uid, department) VALUES (%s, %s);''', (uid, department))
                                                
                                                
                    conn.commit()
                                                    
                                                    
                    if role == 's':
                            cur.execute('''INSERT INTO public.student (sid, grade) VALUES (%s, %s);''', (uid, grade_or_title    ))
                            conn.commit()
                    else:
                            cur.execute('''INSERT INTO public.teacher (id, title) VALUES (%s, %s);''', (uid, grade_or_title)    )
                            conn.commit()
                                                                    
                    ans = "0"
            else :
                    ans = "-1"
                                                                        
            cur.close()
    conn.close()
                                                                                
        return jsonify({
                       'status': ans
        }), 200

def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def create_salt(length = 4):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in xrange(length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt

