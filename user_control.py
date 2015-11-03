#coding:utf-8

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import logging
from tornado.options import options
from tornado.options import define
import os
import sqlite3
import math


settings = dict(
    blog_title="+/- Users",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=True,
#    xsrf_cookies=False,
    cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    autoescape=None,
    debug=True,
)


define("port", default = 8888, help = "run on the given port", type = int)
define("debug", default = 0)

def createUser(self, username):
    errors=[]
    conn = sqlite3.connect('alluser.db')
    cursor = conn.execute("SELECT  name ,passwd from authors order by name")
    lstall = cursor.fetchall()
    lst=[]
    lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
    if username in (user for user,key in lstall):
        errors.append('Account already created')
    if username.strip()== '':
        errors.append('UserName must be input')
    if not errors:
        os.system('useradd -m %s' % username)#add user
        os.system('''su - %s -c "ssh-keygen -q -t dsa -f ~/.ssh/id_dsa -N '' " ''' % username)
        os.system('su - %s -c "cat ~/.ssh/id_dsa.pub > ~/.ssh/authorized_keys"' % username)
        os.system('su - %s -c "chmod 600 ~/.ssh/authorized_keys"' % username)
        os.system('su - %s -c "puttygen -O private -o keyfile.ppk ~/.ssh/id_dsa"' % username)
        os.system('su - %s -c "tar czvf %s.tar keyfile.ppk ~/.ssh/id_dsa"' % (username,username))
        os.system("cp -f /home/%s/%s.tar /root/torna/static"%  (username,username))
        os.system('chsh -s /usr/sbin/nologin %s' % username)#close shell
        conn.execute(
            "INSERT INTO authors (name,passwd) "
            "VALUES (?,?)",
            (username,username+'.tar'))
        conn.commit()
        conn.close()
        errors.append('Success create User:'+username)
    conn = sqlite3.connect('alluser.db')
    cursor = conn.execute("SELECT  name ,passwd from authors  order by name")
    lstall = cursor.fetchall()
    conn.close()
    for count in range(len(lstall)):
        if count < 20:
            lst.append(lstall[count])
    self.render("page.html",lst=lst,lst2=lst2,errors=errors)



def deleteUser(self, username):
    errors=[]
    lst=[]
    conn = sqlite3.connect('alluser.db')
    cursor = conn.execute("SELECT  name,passwd from authors  order by name")
    lstall = cursor.fetchall()
    lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
    conn.close()
    if username:
        allid=username.split(',')
        errors=[]
        for eachid in allid:
            if eachid:
                conn = sqlite3.connect('alluser.db')
                conn.execute(
                    "DELETE FROM authors Where name "
                    " = ?;",
                    (eachid,))
                errors.append('Success delete User:'+eachid)
                os.system('userdel  -r %s' % eachid)#delete user
                conn.commit()
        conn.close()
    else:
        if not (self.get_argument("action_type") =='search' or self.get_argument("action_type") =='create') :
            errors=[]
            errors.append('No user selected')


    conn = sqlite3.connect('alluser.db')
    cursor = conn.execute("SELECT  name ,passwd from authors  order by name")
    lstall = cursor.fetchall()
    conn.close()
    for count in range(len(lstall)):
        if count < 20:
            lst.append(lstall[count])
    self.render("page.html",lst=lst,lst2=lst2,errors=errors)

def searchUser(self, username):
    errors=[]
    lst=[]
    conn = sqlite3.connect('alluser.db')
    cursor = conn.execute("SELECT  name,passwd from authors  order by name")
    lstall = cursor.fetchall()
    lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
    conn.close()
    if not username.lower() in (user.lower() for user,key in lstall):
        # logging.info("current user searched 111 %s", username)
        if username.strip() !=  '':
            errors.append('Account have not created')
        else:
            errors.append('Please enter the UserName you want to search')
    else:
        # logging.info("current user searched 222 %s", username)
        for user,key in lstall:
            if user.lower()==username.lower():
                user = user
                errors.append('''<div><p style = 'color:green;' >Search results are:</p><div><table border =0><tr> <th></th><th align='left'>UserName</th></tr>
                        <tr><td class='cx'><input  type='checkbox' name = "'''+user+'''"></td><td align='left'>'''+user+'''</td>
                        <td align='left'><a href = "/'''+user+'.tar''''">Key</a></td></tr>
			</table></div><div>''')
    for count in range(len(lstall)):
        if count < 20:
            lst.append(lstall[count])
    self.render("page.html",lst=lst,lst2=lst2,errors=errors)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        errors =[]
        lst=[]
        conn = sqlite3.connect('alluser.db')
        cursor = conn.execute("SELECT  name ,passwd from authors order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        conn.close()
        for count in range(len(lstall)):
            if count < 20:
                lst.append(lstall[count])
        self.render("page.html",lst=lst,lst2=lst2,errors=errors)

    def post(self):
        if self.get_argument("action_type") == 'search':
            searchUser(self,self.get_argument("username"))
        elif self.get_argument("action_type") == 'create':
            createUser(self,self.get_argument("username"))
        else:
            deleteUser(self,self.get_argument('action_type'))


class LookHandler(tornado.web.RequestHandler):
    def get(self,n):
        errors =[]
        lst=[]
        conn = sqlite3.connect('alluser.db')
        cursor = conn.execute("SELECT  name,passwd from authors order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        conn.close()
        for i in range(20):
            if (i+(int(n)-1)*20)<len(lstall):
                lst.append(lstall[i+(int(n)-1)*20])
            else:break
        self.render("page.html",lst=lst,lst2=lst2,errors=errors)
             
		
def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/page/(\d+)", LookHandler),
        (r"/(\w+\.tar)",  tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ],**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    logging.info("Web Server Started at %s." % options.port)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
	
	
if __name__ == '__main__':
    main()
