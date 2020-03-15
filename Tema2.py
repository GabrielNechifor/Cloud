import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class WebServer(BaseHTTPRequestHandler):

    connection = mysql.connector.connect(user='root',password='12345', host='localhost', port=3306, database='tema2_cloud')
    connection.autocommit = True
    cursor = connection.cursor()


    def do_GET(self):
        try:
            if self.path == '/anime':
                query = 'select * from anime'
                self.cursor.execute(query)
                response = self.cursor.fetchall()

                if len(response) == 0:
                    self.send_error(404, "Nothing found")
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.send_header('Content-type', 'json/html')
                    to_send = "["
                    for resource in response:
                        resource = self.none_to_null(resource)
                        resource = '{"id":%s, "name":"%s", "episodes":%s}' % (resource[0], resource[1], resource[2])
                        to_send += resource
                        to_send += ","
                    to_send = to_send[:-1]
                    to_send += "]"
                    self.wfile.write(to_send.encode())

            
            elif self.path.startswith('/anime/'):
                parts = self.path.split('/')
                if len(parts) != 3:
                    self.send_error(404, "Invalid path")
                else:
                    id = parts[2]
                    query = 'select * from anime where id = %s' % id
                    self.cursor.execute(query)
                    response = self.cursor.fetchone()
                        
                    if not response:
                        self.send_error(404, "Invalid id")
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.send_header('Content-type', 'json/html')
                        response = self.none_to_null(response)
                        to_send = '{"id":%s, "name":"%s", "episodes":%s}' % (response[0], response[1], response[2])
                        self.wfile.write(to_send.encode())
            else:
                self.send_error(404, "Invalid path")
        except BaseException as e:
            self.send_error(400, 'Invalid format')
            print(e)
                    



    def do_POST(self):
        try:
            if self.path == '/anime':
                query = "SELECT count(*) FROM information_schema.columns WHERE table_name = 'anime';"
                self.cursor.execute(query)
                number_of_columns = self.cursor.fetchone()[0]

                content_length = int(self.headers['Content-Length'])
                post_data_list = json.loads(self.rfile.read(content_length))

                to_send = "["
                for post_data in post_data_list:
                    if 'episodes' not in post_data.keys():
                        post_data['episodes'] = 'null'
                    query = "insert into anime values (null, '%s', %s)" % (post_data['name'], str(post_data['episodes']))
                    self.cursor.execute(query)
                            
                    query = "SELECT LAST_INSERT_ID()"
                    self.cursor.execute(query)
                    id = self.cursor.fetchone()[0]

                    query = "select * from anime where id=" + str(id)
                    self.cursor.execute(query)
                    response = self.cursor.fetchone()
                    response = self.none_to_null(response)
                    response = '{"id":%s, "name":"%s", "episodes":%s}' % (response[0], response[1], response[2]  )

                    to_send += response
                    to_send += ","
                else:
                    to_send = to_send[:-1]
                    to_send += "]"
                    self.send_response(201)
                    self.end_headers()
                    self.send_header('Content-type', 'json/html')
                    self.wfile.write(to_send.encode())

            else:
                self.send_error(404, 'Invalid path')
                        
        except BaseException as e:
            self.send_error(400, "Invalid format")
            print(e)
    


    def do_DELETE(self):
        try:
            if self.path == '/anime':
                self.send_error(403, "Forbidden")
            elif self.path.startswith("/anime/"):

                parts = self.path.split('/')
                if len(parts) != 3:
                    self.send_error(404, "Invalid path")
                else:
                    id = parts[2]
                    
                    query = 'select * from anime where id = %d' % int(id)
                    self.cursor.execute(query)
                    response = self.cursor.fetchall()
                    print(response)
                    
                    if not response:
                        self.send_error(404, "Resource doesn't exist")
                    else:
                        query = 'delete from anime where id = %s' % id
                        self.cursor.execute(query)
                        self.send_response(204)
                        self.end_headers()

                        query = "alter table anime auto_increment = 1;"
                        self.cursor.execute(query)
            else:
                self.send_error(404, 'Invalid path')

        except BaseException as e:
            self.send_error(400, "Invalid format")
            print(e)



    def do_PUT(self):
        try:
            if self.path == '/anime':
                query = "SELECT count(*) FROM information_schema.columns WHERE table_name = 'anime';"
                self.cursor.execute(query)
                number_of_columns = self.cursor.fetchone()[0]

                query = "SELECT count(*) FROM anime;"
                self.cursor.execute(query)
                number_of_lines = self.cursor.fetchone()[0]

                content_length = int(self.headers['Content-Length'])
                post_data_list = json.loads(self.rfile.read(content_length))

                if len(post_data_list) != number_of_lines:
                    raise BaseException()

                for post_data in post_data_list:
                    if len(post_data) != number_of_columns:
                        raise BaseException()
                    else:
                        query = "select * from anime where id ="+ str(post_data['id'])
                        self.cursor.execute(query)
                        response = self.cursor.fetchall()
                        if not response:
                            self.send_error(404, "Given id doesn't exists")
                            break
                        post_data = self.none_to_null(post_data)
                        query = "update anime set name='%s', episodes=%s where id =%s" % (post_data['name'], post_data['episodes'], post_data['id'])
                        self.cursor.execute(query)
                else:
                    self.send_response(204)
                    self.end_headers()
            

            elif self.path.startswith('/anime/'):
                parts = self.path.split('/')
                if len(parts) != 3:
                    self.send_error(404, "Invalid path")
                else:
                    id = parts[2]

                    query = 'select * from anime where id = %d' % int(id)
                    self.cursor.execute(query)
                    response = self.cursor.fetchall()
                    
                    if not response:
                        self.send_error(404, "Id doesn't exist")
                    else:
                        query = "SELECT count(*) FROM information_schema.columns WHERE table_name = 'anime';"
                        self.cursor.execute(query)
                        number_of_columns = self.cursor.fetchone()[0]

                        content_length = int(self.headers['Content-Length'])
                        post_data = json.loads(self.rfile.read(content_length))

                        if len(post_data) != number_of_columns - 1:
                            raise BaseException("invalid number of parameters")
                        else:
                            post_data = self.none_to_null(post_data)
                            query = "update anime set name='%s', episodes=%s where id =%s" % (post_data['name'], post_data['episodes'], id)
                            self.cursor.execute(query)
                            self.send_response(204)
                            self.end_headers()

            else:
                self.send_error(404, "Invalid path")
            

        except BaseException as e:
            self.send_error(400, "Invalid format")
            print(e)



    def do_PATCH(self):
        try:
            if self.path == '/anime':
                query = "SELECT count(*) FROM anime;"
                self.cursor.execute(query)
                number_of_lines = self.cursor.fetchone()[0]

                content_length = int(self.headers['Content-Length'])
                post_data_list = json.loads(self.rfile.read(content_length))

                if len(post_data_list) != number_of_lines:
                    raise BaseException()

                for post_data in post_data_list:
                    query = "select * from anime where id ="+ str(post_data['id'])
                    self.cursor.execute(query)
                    response = self.cursor.fetchall()
                    if response == []:
                        self.send_error(404, "Given id doesn't exists")
                        break

                    key_value = list(post_data.items())
                    key_value  = [(key, (value if value else 'null')) for key,value in key_value]

                    id = post_data['id']
                    for key,value in key_value:
                        if key != 'id':
                            query = "update anime set %s='%s'where id =%d" % (key, str(value) ,int(id))
                            self.cursor.execute(query)
                else:
                    self.send_response(204)
                    self.end_headers()

            elif self.path.startswith('/anime/'):
                parts = self.path.split('/')
                if len(parts) != 3:
                    self.send_error(404, "Invalid path")
                else:
                    id = parts[2]

                    query = 'select * from anime where id = %d' % int(id)
                    self.cursor.execute(query)
                    response = self.cursor.fetchall()
                    
                    if not response:
                        self.send_error(404, "Id doesn't exist")
                    else:
                        content_length = int(self.headers['Content-Length'])
                        post_data = json.loads(self.rfile.read(content_length))

                        key_value = list(post_data.items())
                        key_value  = [(key, (value if value else 'null')) for key,value in key_value]
                        for key,value in key_value:
                            if key != 'id':
                                query = "update anime set %s='%s'where id =%d" % (key, value ,int(id))
                                self.cursor.execute(query)
                        self.send_response(204)
                        self.end_headers()
                            
            else:
                self.send_error(404, "Invalid path")


        except BaseException as e:
            self.send_error(400, "Invalid format")
            print(e)
    


    

    def send_error(self, code, message):
        self.send_response(code)
        self.end_headers()
        self.send_header('Content-type', 'json/html')
        json = '{"message" : "%s"}' % message
        self.wfile.write(json.encode())

    
    def none_to_null(self, items):
        if isinstance(items, tuple):
            items = list(items)
            for index in range(0,len(items)):
                items[index] = items[index] if items[index] else 'null'
        elif isinstance(items, dict):
            for key in items.keys():
                items[key] = items[key] if items[key] else 'null'
        return items



                
        



        
        
        
        
        


http_server = HTTPServer(('localhost', 8080), WebServer)
http_server.serve_forever()