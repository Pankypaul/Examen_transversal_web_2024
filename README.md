Es necesario tener intalado python y virtualenv

1. Una vez descargado el proyecto, se debe crear un ambiente virtual, el nombre recomendado es myvenv ya que el archivo incluye un .gitignore para evitar subir el ambiente.
py -m venv myvenv
2. Se debe actualizar la version de python 
py -m pip install --upgrade pip
3. Luego se debe instalar requeriments.txt
pip install -r requeriments.txt
4. Y por último entrar al ambiente virtual y correr el server.
myvenv/script/activate

py manage.py runserver
