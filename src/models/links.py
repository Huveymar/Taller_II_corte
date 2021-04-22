from src.configs.db import DB
import random

class link:
    def guardar_link(self, link, usuario_id=''):
        codigo = ''

        # algoritmo para generar un codigo de 4 caracteres
        for num in range(4):
            codigo = codigo + chr(int(random.randint(97,122)))
        
        cursor = DB.cursor()

        # validamos si se envio un id de un usuario
        if usuario_id == '':
            cursor.execute("insert into registros(codigo, link) VALUES(?,?)",(codigo, link,))
        else:
            cursor.execute("insert into registros(codigo, link, usuario_id) VALUES(?,?,?)",(codigo, link, usuario_id,))

        cursor.close()

        return codigo
    
    def link_guardado(self, codigo):
        cursor = DB.cursor()
        cursor.execute("select link from registros where codigo=?",(codigo,))
        link = cursor.fetchone()
        cursor.close()

        return link