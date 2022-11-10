from config import *
import datetime

class Usuario(db.Model):
    codigo = db.Column(db.Integer, primary_key = True)
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
    codigo = db.Column(db.Integer, primary_key = True)
    saldo = db.Column(db.Float(10))
    Usuario_id = db.Column(db.Integer, db.ForeignKey(Usuario.codigo), nullable = False)
    usuario = db.relationship("Usuario")

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
    codigo = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    moeda = db.Column(db.String(25))
    valor = db.Column(db.Float(25))
    Conta_id = db.Column(db.Integer, db.ForeignKey(Conta.codigo))
    conta = db.relationship("Conta")
    tipo = db.Column(db.String(10))
    
    __mapper_args__ = {
        'polymorphic_identity':'lancamento',
        'polymorphic_on':'tipo' }

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
    codigo = db.Column(db.Integer, db.ForeignKey(Lancamento.codigo), primary_key = True)
    categoria = db.Column(db.String(250))
    dataVencimento = db.Column(db.Date)
    

    __mapper_args__ = {
        'polymorphic_identity':'despesa'}

    def __str__(self):
        s = f'{self.codigo}, {self.categoria}, {self.descricao}, {self.moeda}, {self.valor}, {self.conta}'
        s += f' | {self.dataVencimento.day}/{self.dataVencimento.month}/{self.dataVencimento.year}'
        return s

    def json(self):
        return {
            "codigo": self.codigo,
            "dataVencimento": self.dataVencimento,
            "categoria": self.categoria
        }

class Receita(Lancamento):
    codigo = db.Column(db.Integer, db.ForeignKey(Lancamento.codigo), primary_key = True)
    dataRecebimento = db.Column(db.Date)

    __mapper_args__ = {
        'polymorphic_identity':'receita'}

    def __str__(self):
        s = f'{self.codigo}, {self.descricao}, {self.moeda}, {self.valor}, {self.conta}'
        s += f' | {self.dataRecebimento.day}/{self.dataRecebimento.month}/{self.dataRecebimento.year}'
        return s

    def json(self):
        return {
            "codigo": self.codigo,
            "dataRecebimento": self.dataRecebimento
        }
if __name__=="__main__":
    os.path.exists(arquivobd)
    os.remove(arquivobd)
    db.create_all()


    U1 = Usuario(email = "generico@gmail.com", senha = "******")
    C1 = Conta(saldo = "1236547890", usuario = U1)
    D1 = Despesa(categoria = "A categoria da despesa (:", dataVencimento = (datetime.date(2014, 1, 25)), descricao = "descricao.despesa", moeda = "real", valor = 25.25, conta = C1)
    R1 = Receita(dataRecebimento = (datetime.date(2014, 1, 26)), descricao = "descricao.receita", moeda = "real", valor = 25.50, conta = C1, )



    db.session.add(U1)
    db.session.commit()
    db.session.add(C1)
    db.session.commit()
    db.session.add(D1)
    db.session.commit()
    db.session.add(R1)
    db.session.commit()

    print(U1)
