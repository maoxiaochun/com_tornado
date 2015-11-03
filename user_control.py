#coding:utf-8

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import logging
from tornado.options import options
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


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        errors =[]
        lst=[]
        conn = sqlite3.connect('alluser.db')
        cursor = conn.execute("SELECT  name ,passwd from authors order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        conn.close()
        for i in range(len(lstall)):
            if i<20:
                lst.append(lstall[i])                   
        self.render("page.html",lst=lst,lst2=lst2,errors=errors)


    def post(self):
        errors=[]
        lst=[]
        conn = sqlite3.connect('alluser.db')
        cursor = conn.execute("SELECT  name,passwd from authors  order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        conn.close()
#        print(self.get_argument("delete_user"))

        username = self.get_argument("username")
        logging.info("current user searched %s", username)
        if self.get_argument("no_user") =='search':#'''Search auth'''
#            print ('search')#
            if not username.lower() in (i.lower() for i,j in lstall):
                logging.info("current user searched 111 %s", username)
   
                if username.strip() !=  '':
                    errors.append('Account have not created')
                else:
                    errors.append('Please enter the UserName you want to search')
            else:
                logging.info("current user searched 222 %s", username)
                errors=[]
                conn = sqlite3.connect('alluser.db')
                sear=conn.execute("SELECT  name, passwd from authors  where name =?",(self.get_argument("username"),))
                lst_sear = sear.fetchall()
                conn.close()
                errors.append('''<div><p style = 'color:green;' >Search results are:</p><div><table border =0><tr> <th></th><th align='left'>UserName</th></tr>
			<tr><td class='cx'><input  type='checkbox' name = "'''+self.get_argument("username")+'''"></td><td align='left'>'''+self.get_argument("username")+'''</td>
                        <td align='left'><a href = "/'''+self.get_argument("username")+'.tar''''">Key</a></td></tr>
			</table></div><div>''')
        elif self.get_argument("no_user") =='create':#'''add auth'''	
            errors=[]
#            print ('create')#
            conn = sqlite3.connect('alluser.db')
            cursor = conn.execute("SELECT  name ,passwd from authors order by name")
            lstall = cursor.fetchall()
            lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
            if self.get_argument("username") in (i for i,j in lstall):
                errors.append('Account already created')
            if self.get_argument("username").strip()== '':
                errors.append('UserName must be input')
            if not errors:
                os.system('useradd -m %s' % self.get_argument("username"))#add user
                os.system('''su - %s -c "ssh-keygen -q -t dsa -f ~/.ssh/id_dsa -N '' " ''' % self.get_argument("username"))
                os.system('su - %s -c "cat ~/.ssh/id_dsa.pub > ~/.ssh/authorized_keys"' % self.get_argument("username"))
                os.system('su - %s -c "chmod 600 ~/.ssh/authorized_keys"' % self.get_argument("username"))
                os.system('su - %s -c "puttygen -O private -o keyfile.ppk ~/.ssh/id_dsa"' % self.get_argument("username"))
                os.system('su - %s -c "tar czvf %s.tar keyfile.ppk ~/.ssh/id_dsa"' % (self.get_argument("username"),self.get_argument("username")))
                os.system("cp -f /home/%s/%s.tar /root/torna/static"%  (self.get_argument("username"),self.get_argument("username")))
                
                key_ppk=os.popen('su - %s -c "cat keyfile.ppk"' % self.get_argument("username"))
                key_dsa=os.popen('su - %s -c "cat ~/.ssh/id_dsa"' % self.get_argument("username"))
                print('key was:',list(key_ppk),key_dsa)#############
                os.system('chsh -s /usr/sbin/nologin %s' % self.get_argument("username"))#close shell
                conn.execute(
                    "INSERT INTO authors (name,passwd) "
                    "VALUES (?,?)",
                    (self.get_argument("username"),self.get_argument("username")+'.tar'))
                conn.commit()
                conn.close()
                errors.append('Success create User:'+self.get_argument("username"))
        if self.get_argument("delete_user") =='quit':
            pass
        elif self.get_argument("delete_user"):
            allid=self.get_argument("delete_user").split(',')
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
            if not (self.get_argument("no_user") =='search' or self.get_argument("no_user") =='create') :
                errors=[]
                errors.append('No user selected')
            

        conn = sqlite3.connect('alluser.db')
        cursor = conn.execute("SELECT  name ,passwd from authors  order by name")
        lstall = cursor.fetchall()
        conn.close()
        for i in range(len(lstall)):
            if i<20:
                lst.append(lstall[i])
        self.render("page.html",lst=lst,lst2=lst2,errors=errors)

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
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
	
	
if __name__ == '__main__':
    main()
