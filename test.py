import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import options
import os
import sqlite3
import math



settings = dict( 
    blog_title="+/- Authors", 
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
        cursor = conn.execute("SELECT  name, passwd from authors order by name")
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
        cursor = conn.execute("SELECT  name, passwd from authors  order by name")
        lstall = cursor.fetchall()
        lst2 = range(1,int(math.ceil(len(lstall)/20))+2)
        print(self.get_argument("delete_user"))
        if self.get_argument("delete_user"):
            conn.execute(
                "DELETE FROM authors Where name "
                " = ?;",
                (self.get_argument("delete_user"),))
            conn.commit()
            errors.append('Success delete User:'+self.get_argument("delete_user"))
            conn.close()
        else:
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
        self.render("page.html",lst=lst,lst2=lst2,errors=errors)

class LookHandler(tornado.web.RequestHandler):
    def get(self,n):
        errors =[]
        lst=[]
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name, passwd from authors order by name")
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
    def post(self):
        errors=[]
        lst=[]
        lst_sear=[]
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT  name, passwd from authors  order by name")
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
        cursor = conn.execute("SELECT  name, passwd from authors")
        lst = cursor.fetchall()
        if self.get_argument("username") in (i for i,j in lst):
            errors.append('Account already created')
        if self.get_argument("username").strip()== '':
            errors.append('UserName must be input')
        if self.get_argument("password").strip() ==  '' :
            errors.append('Password must be input')
        if not self.get_argument("password") == self.get_argument("password2"):
            errors.append('The passwords you entered must be the same')
        if not errors:
            conn.execute(
                "INSERT INTO authors (name, passwd) "
                "VALUES (?, ?)",
                (self.get_argument("username"),
                self.get_argument("password")))
            conn.commit()
            errors.append('Success create User:'+self.get_argument("username"))
        conn.close()
        self.render("create_author.html",errors=errors)
        

#'''delete auth'''
class AuthDeleteHandler(tornado.web.RequestHandler):
    def get(self):
        errors=[]
        self.render("delete_author.html",errors=errors)

    def post(self):
        errors=[]
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()
        cur1 = conn.execute("SELECT  name, passwd from authors")
        lst = cur1.fetchall()
        if not self.get_argument("username")  in (i for i,j in lst):
            if self.get_argument("username").strip() !=  '':
                errors.append('Account not created')
            else:
                errors.append('Enter the UserName you want to delete')
        if not errors:
            cur.execute(
                "DELETE FROM authors Where name "
                " = ?;",
                (self.get_argument("username"),))
            conn.commit()
            errors.append('Success delete User:'+self.get_argument("username"))
        conn.close()
        self.render("delete_author.html",errors=errors)
		
def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/page/(\d+)", LookHandler),
        (r"/auth/search", AuthSearchHandler),
        (r"/auth/create", AuthCreateHandler),
        (r"/auth/delete", AuthDeleteHandler),
		
    ],**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
	
	
if __name__ == '__main__':
    main()
