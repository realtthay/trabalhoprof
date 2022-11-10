from config import *
from modelo import Usuario, Conta, Despesa, Receita
from datetime import date

@app.route("/")
def inicio():
    return 'backend operante.'

@app.route("/listar/<string:classe>")
def listar(classe):
    if classe == "Usuario":
      dados = db.session.query(Usuario).all()
    elif classe == "Conta":
      dados = db.session.query(Conta).all()
    elif classe == "Despesa":
      dados = db.session.query(Despesa).all()
    elif classe == "Receita":
      dados = db.session.query(Receita).all()
    
    lista_jsons = [ x.json() for x in dados ]
    resposta = jsonify(lista_jsons)
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta

#curl localhost:5000/listar/Usuario
#curl localhost:5000/listar/Conta
#curl localhost:5000/listar/Despesa
#curl localhost:5000/listar/Receita

@app.route("/incluir/<string:classe>")
def incluir(classe):
    resposta = jsonify({"resultado": "ok", "detalhes": "ok"})

    if classe == "Usuario":
      dados = request.get_json(Usuario)
      try: 
          nova = Usuario(**dados) 
          db.session.add(nova) 
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})

    elif classe == "Conta":
      dados = request.get_json(Conta)
      try: 
          nova = Conta(**dados) 
          db.session.add(nova) 
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})
    elif classe == "Despesa":
      dados = request.get_json(Despesa)
      partes = dados['dataVencimento'].split("-")
      dados['dataVencimento'] = date(int(partes[0]), int(partes[1]), int(partes[2]))
      try: 
          nova = Despesa(**dados) 
          db.session.add(nova) 
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})
    elif classe == "Receita":
      dados = request.get_json(Receita)
      partes = dados['dataRecebimento'].split("-")
      dados['dataRecebimento'] = date(int(partes[0]), int(partes[1]), int(partes[2]))
      try: 
          nova = Receita(**dados) 
          db.session.add(nova) 
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})
    
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta
  
#curl -d '{"email": "teste@gmail.com", "senha": "*******"}' -X GET -H "Content-Type:application/json" localhost:5000/incluir/Usuario
#curl -d '{"saldo": "1050.25", "Usuario_id": "1"}' -X GET -H "Content-Type:application/json" localhost:5000/incluir/Conta
#curl -d '{"categoria": "incluido", "dataVencimento": "2015-12-19"}' -X GET -H "Content-Type:application/json" localhost:5000/incluir/Despesa 
#curl -d '{"dataRecebimento": "2018-03-29"}' -X GET -H "Content-Type:application/json" localhost:5000/incluir/Receita

@app.route("/excluir/<string:classe>/<int:Codigo>", methods = ['DELETE'])
def excluir(classe, Codigo):
    resposta = jsonify({"resultado": "ok", "detalhes": "ok"})
    
    if classe == "Usuario":
      try: 
          Usuario.query.filter(Usuario.codigo == Codigo).delete()
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})

    elif classe == "Conta":
      try: 
          Conta.query.filter(Conta.codigo == Codigo).delete()
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})
      
    elif classe == "Despesa":
      try: 
          Despesa.query.filter(Despesa.codigo == Codigo).delete()
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})
    
    elif classe == "Receita":
      try: 
          Receita.query.filter(Receita.codigo == Codigo).delete()
          db.session.commit() 
      except Exception as e: 
          resposta = jsonify({"resultado":"erro", "detalhes":str(e)})

    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta

#curl -X DELETE localhost:5000/excluir/Usuario/2
#curl -X DELETE localhost:5000/excluir/Conta/2
#curl -X DELETE localhost:5000/excluir/Despesa/2
#curl -X DELETE localhost:5000/excluir/Receita/2

@app.route("/atualizar/<string:classe>", methods = ['PUT'])
def atualizar(classe):
    resposta = jsonify({"resultado": "ok", "detalhes": "ok"})
    dados = request.get_json() 
    if classe == "Usuario":
      try:
        if 'codigo' not in dados:
          resposta = jsonify({"resultado": "erro", 
          "detalhes": "Atributo codigo não encontrado"})
        else:
          Codigo = dados['codigo']
          alguem = Usuario.query.get(Codigo)
          if alguem is None:
            resposta = jsonify({"resultado": "erro", 
            "detalhes": f"Objeto não encontrado, codigo: {Codigo}"})
          else:
            alguem.email = dados['email']
            alguem.senha = dados['senha']
            db.session.commit()
      except Exception as e:
        resposta = jsonify({"resultado": "erro", "detalhes": str(e)})
    
    elif classe == "Conta":
      try:
        if 'codigo' not in dados:
          resposta = jsonify({"resultado": "erro", 
          "detalhes": "Atributo codigo não encontrado"})
        else:
          Codigo = dados['codigo']
          alguem = Conta.query.get(Codigo)
          if alguem is None:
            resposta = jsonify({"resultado": "erro", 
            "detalhes": f"Objeto não encontrado, codigo: {Codigo}"})
          else:
            alguem.saldo = dados['saldo']
            alguem.Usuario_id = dados['Usuario_id']
            db.session.commit()
      except Exception as e:
        resposta = jsonify({"resultado": "erro", "detalhes": str(e)})
    
    elif classe == "Despesa":
      try:
        if 'codigo' not in dados:
          resposta = jsonify({"resultado": "erro", 
          "detalhes": "Atributo codigo não encontrado"})
        else:
          Codigo = dados['codigo']
          alguem = Despesa.query.get(Codigo)
          if alguem is None:
                  resposta = jsonify({"resultado": "erro", 
                  "detalhes": f"Objeto não encontrado, codigo: {Codigo}"})
          else:
                  alguem.categoria = dados['categoria']
                  partes = dados['dataVencimento'].split("-")
                  alguem.dataVencimento = dados['dataVencimento'] = date(int(partes[0]), int(partes[1]), int(partes[2]))
                  db.session.commit()
      except Exception as e:
        resposta = jsonify({"resultado": "erro", "detalhes": str(e)})
    
    elif classe == "Receita":
      try:
        if 'codigo' not in dados:
          resposta = jsonify({"resultado": "erro", 
          "detalhes": "Atributo codigo não encontrado"})
        else:
          Codigo = dados['codigo']
          alguem = Receita.query.get(Codigo)
          if alguem is None:
                  resposta = jsonify({"resultado": "erro", 
                  "detalhes": f"Objeto não encontrado, codigo: {Codigo}"})
          else:
                  partes = dados['dataRecebimento'].split("-")   
                  alguem.dataRecebimento = dados['dataRecebimento'] = date(int(partes[0]), int(partes[1]), int(partes[2])) 
                  db.session.commit()
      except Exception as e:
        resposta = jsonify({"resultado": "erro", "detalhes": str(e)}) 
    else:
        resposta = jsonify({"resultado": "erro", "detalhes": f"Classe não encontrada: {classe}"})

    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta        

#curl -X PUT -d '{"codigo":2, "email":"atualizado@gmail.com", "senha":"********"}' -H "Content-Type:application/json" localhost:5000/atualizar/Usuario
#curl -X PUT -d '{"codigo":2, "saldo": "1050.25", "Usuario_id": "1"}' -H "Content-Type:application/json" localhost:5000/atualizar/Conta

#curl -X PUT -d '{"codigo":1, "categoria": "atualizado", "dataVencimento": "2016-07-13"}' -H "Content-Type:application/json" localhost:5000/atualizar/Despesa

#curl -X PUT -d '{"codigo":2, "dataRecebimento": "2018-05-24"}' -H "Content-Type:application/json" localhost:5000/atualizar/Receita
      

app.run()