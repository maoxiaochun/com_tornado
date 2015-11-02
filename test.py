import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import options
import os
import sqlite3
import math



settings = dict( 
    blog_title="+/- Users", 
    template_path=os.path.join(os.path.dirname(__file__), "templates"), 
    static_path=os.path.join(os.path.dirname(__file__), "static"), 
#    xsrf_cookies=True,
    xsrf_cookies=False,
    cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__", 
    autoescape=None, 
    debug=True, 
)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        errors =[]
        lst=[]
        conn = sqlite3.connect('test.db')
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
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name,passwd from authors  order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        conn.close()
#        print(self.get_argument("delete_user"))

        if self.get_argument("no_user") =='search':
            print 'search'#
            if not self.get_argument("username") in (i for i,j in lstall):
                if self.get_argument("username").strip() !=  '':
                    errors.append('Account have not created')
                else:
                    errors.append('Please enter the UserName you want to search')
            else:
                errors=[]
                conn = sqlite3.connect('test.db')
                sear=conn.execute("SELECT  name, passwd from authors  where name =?",(self.get_argument("username"),))
                lst_sear = sear.fetchall()
                conn.close()
                errors.append('''<div><p style = 'color:green;' >Search results are:</p><div><table border =0><tr> <th></th><th align='left'>UserName</th></tr>
			<tr><td class='cx'><input  type='checkbox' name = "'''+self.get_argument("username")+'''"></td><td align='left'>'''+self.get_argument("username")+'''</td></tr>
			</table></div><div>''')
                for i in range(len(lstall)):
                    if i<20:
                        lst.append(lstall[i])
                self.render("page.html",lst=lst,lst2=lst2,lst_sear=lst_sear,errors=errors)
        elif self.get_argument("no_user") =='create':
            errors=[]
            print 'create'#
            conn = sqlite3.connect('test.db')
            cursor = conn.execute("SELECT  name ,passwd from authors order by name")
            lstall = cursor.fetchall()
            lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
            if self.get_argument("username") in (i for i,j in lstall):
                errors.append('Account already created')
            if self.get_argument("username").strip()== '':
                errors.append('UserName must be input')
            if not errors:
                conn.execute(
                    "INSERT INTO authors (name,passwd) "
                    "VALUES (?,'defult')",
                    (self.get_argument("username"),))
                conn.commit()
                conn.close()
                os.system('useradd -m %s' % self.get_argument("username"))#add user
                os.system('chsh -s /usr/sbin/nologin %s' % self.get_argument("username"))#close shell
                errors.append('Success create User:'+self.get_argument("username"))
                conn = sqlite3.connect('test.db')
                cursor = conn.execute("SELECT  name ,passwd from authors  order by name")
                lstall = cursor.fetchall()
                conn.close()
            for i in range(len(lstall)):
                if i<20:
                    lst.append(lstall[i])
            self.render("page.html",lst=lst,lst2=lst2,errors=errors)

        if self.get_argument("delete_user") =='quit':
            pass
        elif self.get_argument("delete_user"):
            errors=[]
            conn = sqlite3.connect('test.db')
            conn.execute(
                "DELETE FROM authors Where name "
                " = ?;",
                (self.get_argument("delete_user"),))
            conn.commit()
            errors.append('Success delete User:'+self.get_argument("delete_user"))
#            os.system('')
#            os.system('sudo su - ')#swith root
#            os.system('')#passwd
            os.system('userdel %s' % self.get_argument("delete_user"))#delete user
            conn.close()
        else:
            if not self.get_argument("no_user") =='search':
                errors=[]
                errors.append('No user selected')
            

        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name ,passwd from authors  order by name")
        lstall = cursor.fetchall()
        conn.close()
        for i in range(len(lstall)):
            if i<20:
                lst.append(lstall[i])
        self.render("page.html",lst=lst,lst2=lst2,errors=errors)



class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        errors =[]
        lst=[]
        conn = sqlite3.connect('test.db')
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
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name,passwd from authors  order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
#        print(self.get_argument("delete_user"))
        if self.get_argument("delete_user") =='quit':
            pass
        elif self.get_argument("delete_user"):
            conn.execute(
                "DELETE FROM authors Where name "
                " = ?;",
                (self.get_argument("delete_user"),))
            conn.commit()
            errors.append('Success delete User:'+self.get_argument("delete_user"))
#            os.system('')
#            os.system('sudo su - ')#swith root
#            os.system('')#passwd
            os.system('userdel %s' % self.get_argument("delete_user"))#delete user
        else:
            errors.append('No user selected')
        conn.close()
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name,passwd from authors  order by name")
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
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name,passwd from authors order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        conn.close()
        for i in range(20):
            if (i+(int(n)-1)*20)<len(lstall):
                lst.append(lstall[i+(int(n)-1)*20])
            else:break
        self.render("page.html",lst=lst,lst2=lst2,errors=errors)

        
#'''Search auth'''		
class AuthSearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("search_author1.html")
        
    def post(self):
        errors=[]
        lst=[]
        lst_sear=[]
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name,passwd from authors  order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        for i in range(20):
            if i<len(lstall):
                lst.append(lstall[i])
        if not self.get_argument("username") in (i for i,j in lstall):
            if self.get_argument("username").strip() !=  '':
                errors.append('Account have not created')
            else:
                errors.append('Please enter the UserName you want to search')
        else:
            sear=conn.execute("SELECT  name, passwd from authors  where name =?",(self.get_argument("username"),))
            lst_sear = sear.fetchall()
            conn.close()
            self.render("search_author.html",lst_sear=lst_sear,errors=errors)
        conn.close()
        self.render("search_author.html",lst_sear=lst_sear,errors=errors)

#'''add auth'''	
class AuthCreateHandler(tornado.web.RequestHandler):
    def get(self):
        errors=[]
        self.render("create_author.html",errors=errors)

    def post(self):
        errors=[]
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name,passwd from authors")
        lst = cursor.fetchall()
        if self.get_argument("username") in (i for i,j in lst):
            errors.append('Account already created')
        if self.get_argument("username").strip()== '':
            errors.append('UserName must be input')
        if not errors:
            conn.execute(
                "INSERT INTO authors (name, passwd) "
                "VALUES (?)",
                (self.get_argument("username"),))
            conn.commit()
#            os.system('sudo su - ')#swith root
#            os.system('zhangchun')#passwd
            os.system('useradd -m %s' % self.get_argument("username"))#add user
#            os.system('passwd %s' % self.get_argument("username"))
#            os.system('%s' % self.get_argument("password"))
#            os.system('%s' % self.get_argument("password"))
            os.system('chsh -s /usr/sbin/nologin %s' % self.get_argument("username"))#close shell
#            os.system('su - %s'% self.get_argument("username"))
            errors.append('Success create User:'+self.get_argument("username"))
        conn.close()
        self.render("create_author.html",errors=errors)
		
   
		
def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/page/(\d+)", LookHandler),
        (r"/auth/search", AuthSearchHandler),
        (r"/auth/create", AuthCreateHandler),
        (r"/auth/delete", DetailHandler),

    ],**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
	
	
if __name__ == '__main__':
    main()
