# Como executar o projeto:

## 1. Tenha o [Python](https://www.python.org/downloads/) instalado em seu computador.

## 2. Abra o terminal do seu sistema.

## 3. Clone o repositório do GitHub com o seguinte comando:

```
git clone https://github.com/Code-Nine-FTC/Grupo-Code-Nine
```
## 4. Navegue para a pasta da aplicação:
```
cd Grupo-Code-Nine/src
```
## 5. Crie e inicie o ambiente virtual:
```
python -m venv venv
.\venv\Scripts\activate
```
Caso esteja utilizando linux:
```
python3 -m venv venv
source venv\bin\activate
```
## 6. Instale o flask e os componentes necessários:
```
pip install -r req.txt
```

## 7. Antes de executar, verifique se a senha do arquivo app.py (localizado dentro da pasta src) coincide com sua senha do MySQL (definimos por padrão "fatec", você pode alterá-la de acordo com a senha definida na instalação do MySQL). 
```
#Defina os seguintes valores de acordo com seu usuário do seu MYSQL
db = {
    'host': "localhost", #host = ip, no caso localhost
    'user': "root", #usuario para logar
    'password': "fatec", #senha 
    'database': "cianp", #qual banco de dados será utilizado
} 
```

## 8. Execute a aplicação com o comando: 
```   
flask run
```

## 9. Agora, abra o seguinte link no navegador de sua preferência: http://127.0.0.1:5000 

<br>

## 10. Após utilizar o site, utilize esse comando no terminal para fechar o ambiente virtual:
```
deactivate
``` 

<br>

