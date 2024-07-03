Es necesario tener intalado python y virtualenv

1. Una vez descargado el proyecto, se debe crear un ambiente virtual, el nombre recomendado es myvenv ya que el archivo incluye un .gitignore para evitar subir el ambiente.
2. py -m venv myvenv
3. Se debe actualizar la version de python
4. py -m pip install --upgrade pip
5. Luego se debe instalar requeriments.txt
6. pip install -r requeriments.txt
7. Y por último entrar al ambiente virtual y correr el server.
8. myvenv/script/activate
9. py manage.py runserver
