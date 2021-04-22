from src.configs.db import DB
from hashlib import md5

class usuario:
    def guardar_usuario(self, nombre, email, password):
        cursor = DB.cursor()
        password = md5(password.encode("utf-8")).hexdigest()
        
        cursor.execute("insert into usuarios(nombre, correo, password) values(?,?,?)", (nombre,email,password,))
        cursor.close()

    def fecha_confirmacion(self, email):
        cursor = DB.cursor()
        cursor.execute("update usuarios set fecha_confirmacion=CURDATE() where correo=?", (email,))
        cursor.close()
    
    def validar_fecha(self, email):
        cursor = DB.cursor()
        cursor.execute("select fecha_confirmacion from usuarios where correo=?", (email,))
        registros = cursor.fetchone()
        cursor.close()

        return registros
    
    def validar_usuario(self, email, password):
        cursor = DB.cursor()
        password = md5(password.encode("utf-8")).hexdigest()

        cursor.execute("select id, nombre from usuarios where correo=? and password=?", (email,password,))
        registros = cursor.fetchone()
        cursor.close()

        return registros
    
    def links_guardados(self, id):
        cursor = DB.cursor()

        cursor.execute("select * from registros where usuario_id=?", (id,))
        registros = cursor.fetchall()
        cursor.close()

        return registros
    
    def eliminar_link(self, id):
        cursor = DB.cursor()
        cursor.execute("delete from registros  where id=?", (id,))
        cursor.close()
    
    def editar_link(self, id, link):
        cursor = DB.cursor()
        cursor.execute("update registros set link=? where id=?", (link,id,))
        cursor.close()