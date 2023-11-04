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

<h5> 7. Antes de executar, verifique se a senha do arquivo app.py (localizado dentro da pasta src) coincide com sua senha do MySQL (definimos por padrão "12345", você pode alterá-la de acordo com a senha definida na instalação do MySQL). </h5>
    
    #Defina a senha abaixo de acordo com seu MySQL:
    app.config["MYSQL_PASSWORD"] = "12345"
    
<h6> 7.1. Exemplo: Digamos que sua senha do MySQL seja " abcd ", você substiuirá a senha por: </h6>
    
    #Defina a senha abaixo de acordo com seu MySQL:
    app.config["MYSQL_PASSWORD"] = "abcd"

<h5> 8. Execute a aplicação com o comando: </h5>
    
    flask run

<h5> 9. Agora, abra o seguinte link no navegador de sua preferência: http://127.0.0.1:5000 </h5>

<h5> 10. Após utilizar o site, utilize esse comando no terminal para fechar o ambiente virtual:

    deactivate
 
<br>

