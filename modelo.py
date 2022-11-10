class Usuario(db.Model):
    codigo = db.Collumn(db.Integer, primary_Key = True)
    email = db.Column(db.String(250))
    senha = db.Column(db.String(250))

    def __str__(self):
        return str(self.codigo) + "," + self.email + "," + self.senha

    def json(self):
        return {
            "codigo": self.codigo,
            "email": self.email,
            "senha": self.senha
        }

class Conta(db.Model):
    codigo = db.Collumn(db.Integer, primary_Key = True)
    saldo = db.Column(db.Float(10))
    Usuario_id = db.Column(db.Integer, db.ForeignKey(Usuario.codigo), nullable = False)
    usuario = db.Relationship("Usuario")

    def __str__(self):
        return str(self.codigo) + "," + self.saldo + "," + self.usuario

    def json(self):
        return {
            "codigo": self.codigo,
            "saldo": self.saldo,
            "Usuario_id": self.Usuario_id,
            "usuario": self.usuario.json()
        }

class Lancamento(db.Model):
    codigo = db.Collumn(db.Integer, primary_Key = True)
    descricao = db.Column(db.String(250))
    moeda = db.Column(db.String(25))
    valor = db.Column(db.Integer(25))
    Conta_id = db.Column(db.Integer, db.ForeignKey(Conta.codigo), nullable = False)
    conta = db.Relationship("Conta")
    tipo = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic-identity:lancamento'
        'polymorphic-on:tipo' }

    def __str__(self):
        return str(self.codigo) + "," + self.descricao + "," + self.moeda + "," + self.valor + "," + self.conta

    def json(self):
        return {
            "codigo": self.codigo,
            "descricao": self.descricao,
            "moeda": self.moeda,
            "valor": self.valor,
            "Conta_id": self.Conta_id,
            "conta": self.conta.json()
        }

class Despesa(Lancamento):
    codigo = db.Column(db.Integer, db.ForeignKey(Lancamento.codigo), primary_Key = True)
    categoria = db.Column(db.String(250))
    dataVencimento = db.Column(db.Date)
    

    __mapper_args__ = {
        'polymorphic-identity:despesa'}

    def __str__(self):
        s = f'{self.codigo}, {self.categoria}'
        s += f' | {self.dataVencimento.day}/{self.dataVencimento.month}/{self.dataVencimento.year}'
        return s

    def json(self):
        return {
            "codigo": self.codigo,
            "dataVencimento": self.dataVencimento,
            "categoria": self.categoria
        }

class Receita(Lancamento):
    codigo = db.Column(db.Integer, db.ForeignKey(Lancamento.codigo), primary_Key = True)
    dataRecebimento = db.Column(db.Date)

    __mapper_args__ = {
        'polymorphic-identity:receita'}

    def __str__(self):
        s = f'{self.codigo}, '
        s += f' | {self.dataRecebimento.day}/{self.dataRecebimento.month}/{self.dataRecebimento.year}'
        return s

    def json(self):
        return {
            "codigo": self.codigo,
            "dataRecebimento": self.dataRecebimento
        }

#data = date(2014, 1, 25),