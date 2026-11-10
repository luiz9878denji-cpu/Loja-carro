from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent
BANCO = BASE_DIR / "autoprime.db"
app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-por-uma-chave-secreta-forte-antes-de-publicar"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

CARROS = [{'id': 1, 'nome': 'BMW 320i', 'preco': 289900.0, 'imagem': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Sedã esportivo com acabamento premium e tecnologia moderna.', 'motor': '2.0 Turbo', 'potencia': '184 cv', 'velocidade': '235 km/h', 'acessorios': [{'nome': 'Teto solar', 'preco': 8500}, {'nome': 'Bancos em couro', 'preco': 6200}, {'nome': 'Sistema de som premium', 'preco': 4900}], 'imagens_cores': {}, 'categoria': 'Sedã'}, {'id': 2, 'nome': 'Ford Mustang', 'preco': 529900.0, 'imagem': 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Esportivo marcante, com desempenho e design imponente.', 'motor': '5.0 V8', 'potencia': '480 cv', 'velocidade': '250 km/h', 'acessorios': [{'nome': 'Escape esportivo', 'preco': 12500}, {'nome': 'Rodas especiais', 'preco': 16800}, {'nome': 'Bancos esportivos', 'preco': 9200}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 3, 'nome': 'Porsche 911', 'preco': 899900.0, 'imagem': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Esportivo de alto desempenho com design icônico.', 'motor': '3.0 Boxer biturbo', 'potencia': '385 cv', 'velocidade': '293 km/h', 'acessorios': [{'nome': 'Pacote Sport', 'preco': 18900}, {'nome': 'Freios esportivos', 'preco': 24500}, {'nome': 'Interior premium', 'preco': 21500}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 4, 'nome': 'Mercedes-Benz C300', 'preco': 389900.0, 'imagem': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Conforto, sofisticação e tecnologia em um sedã premium.', 'motor': '2.0 Turbo', 'potencia': '258 cv', 'velocidade': '250 km/h', 'acessorios': [{'nome': 'Teto panorâmico', 'preco': 11900}, {'nome': 'Pacote de iluminação', 'preco': 5400}, {'nome': 'Assistente de estacionamento', 'preco': 7800}], 'imagens_cores': {}, 'categoria': 'Sedã'}, {'id': 5, 'nome': 'Audi R8', 'preco': 1199900.0, 'imagem': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Superesportivo com linhas agressivas e desempenho elevado.', 'motor': '5.2 V10', 'potencia': '570 cv', 'velocidade': '324 km/h', 'acessorios': [{'nome': 'Pacote carbono', 'preco': 28500}, {'nome': 'Rodas forjadas', 'preco': 32000}, {'nome': 'Som premium', 'preco': 7900}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 6, 'nome': 'Range Rover Evoque', 'preco': 399900.0, 'imagem': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV sofisticado, versátil e confortável para o dia a dia.', 'motor': '2.0 Turbo', 'potencia': '249 cv', 'velocidade': '230 km/h', 'acessorios': [{'nome': 'Teto panorâmico', 'preco': 11900}, {'nome': 'Pacote off-road', 'preco': 15400}, {'nome': 'Bancos aquecidos', 'preco': 6300}], 'imagens_cores': {}, 'categoria': 'SUV'}, {'id': 7, 'nome': 'Toyota Corolla GR-S', 'preco': 189900.0, 'imagem': 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Sedã moderno com conforto, eficiência e visual esportivo.', 'motor': '2.0 Flex', 'potencia': '177 cv', 'velocidade': '210 km/h', 'acessorios': [{'nome': 'Teto solar', 'preco': 7900}, {'nome': 'Kit esportivo', 'preco': 6500}, {'nome': 'Central multimídia premium', 'preco': 3800}], 'imagens_cores': {}, 'categoria': 'Sedã'}, {'id': 8, 'nome': 'Honda Civic Type R', 'preco': 429900.0, 'imagem': 'https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Esportivo de alto desempenho com acerto voltado para condução dinâmica.', 'motor': '2.0 Turbo', 'potencia': '297 cv', 'velocidade': '275 km/h', 'acessorios': [{'nome': 'Aerofólio esportivo', 'preco': 8900}, {'nome': 'Rodas especiais', 'preco': 14500}, {'nome': 'Escape esportivo', 'preco': 11200}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 9, 'nome': 'Chevrolet Camaro SS', 'preco': 499900.0, 'imagem': 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Muscle car com motor V8 e presença marcante.', 'motor': '6.2 V8', 'potencia': '461 cv', 'velocidade': '290 km/h', 'acessorios': [{'nome': 'Faixas esportivas', 'preco': 4200}, {'nome': 'Escape performance', 'preco': 13900}, {'nome': 'Rodas aro especial', 'preco': 17200}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 10, 'nome': 'Lamborghini Huracán', 'preco': 3290000.0, 'imagem': 'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Superesportivo italiano com design marcante e motor aspirado.', 'motor': '5.2 V10', 'potencia': '640 cv', 'velocidade': '325 km/h', 'acessorios': [{'nome': 'Pacote em fibra de carbono', 'preco': 85000}, {'nome': 'Freios carbono-cerâmica', 'preco': 72000}, {'nome': 'Interior personalizado', 'preco': 49000}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 11, 'nome': 'Ferrari 488 GTB', 'preco': 2890000.0, 'imagem': 'https://images.unsplash.com/photo-1592198084033-a562f1a6a5a5?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Esportivo italiano que combina desempenho, tecnologia e exclusividade.', 'motor': '3.9 V8 biturbo', 'potencia': '670 cv', 'velocidade': '330 km/h', 'acessorios': [{'nome': 'Pacote aerodinâmico', 'preco': 65000}, {'nome': 'Rodas forged', 'preco': 38000}, {'nome': 'Bancos racing', 'preco': 27000}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 12, 'nome': 'Jeep Wrangler Rubicon', 'preco': 459900.0, 'imagem': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV 4x4 preparado para aventuras dentro e fora da estrada.', 'motor': '2.0 Turbo', 'potencia': '272 cv', 'velocidade': '180 km/h', 'acessorios': [{'nome': 'Kit off-road', 'preco': 18500}, {'nome': 'Guincho dianteiro', 'preco': 9200}, {'nome': 'Capota premium', 'preco': 11500}], 'imagens_cores': {}, 'categoria': 'SUV'}, {'id': 13, 'nome': 'Toyota Hilux SRX', 'preco': 329900.0, 'imagem': 'https://images.unsplash.com/photo-1551830820-330a71b99659?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Picape robusta para trabalho, viagens e uso diário.', 'motor': '2.8 Turbo Diesel', 'potencia': '204 cv', 'velocidade': '180 km/h', 'acessorios': [{'nome': 'Capota marítima', 'preco': 3200}, {'nome': 'Santo antônio', 'preco': 2800}, {'nome': 'Estribo lateral', 'preco': 2400}], 'imagens_cores': {}, 'categoria': 'Picape'}, {'id': 14, 'nome': 'Volvo XC60', 'preco': 429900.0, 'imagem': 'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV premium com foco em conforto, tecnologia e segurança.', 'motor': '2.0 híbrido', 'potencia': '462 cv', 'velocidade': '180 km/h', 'acessorios': [{'nome': 'Teto panorâmico', 'preco': 12500}, {'nome': 'Som premium', 'preco': 9800}, {'nome': 'Pacote de acabamento', 'preco': 7200}], 'imagens_cores': {}, 'categoria': 'SUV'}, {'id': 15, 'nome': 'Audi Q5', 'preco': 389900.0, 'imagem': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV sofisticado com dirigibilidade equilibrada e tecnologia embarcada.', 'motor': '2.0 Turbo', 'potencia': '265 cv', 'velocidade': '240 km/h', 'acessorios': [{'nome': 'Teto panorâmico', 'preco': 10900}, {'nome': 'Pacote S line', 'preco': 14800}, {'nome': 'Som premium', 'preco': 6500}], 'imagens_cores': {}, 'categoria': 'SUV'}, {'id': 16, 'nome': 'Nissan GT-R', 'preco': 1190000.0, 'imagem': 'https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Esportivo japonês conhecido pela tração integral e desempenho impressionante.', 'motor': '3.8 V6 biturbo', 'potencia': '570 cv', 'velocidade': '315 km/h', 'acessorios': [{'nome': 'Kit aerodinâmico', 'preco': 24500}, {'nome': 'Escape titanium', 'preco': 18900}, {'nome': 'Rodas forged', 'preco': 21500}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 17, 'nome': 'Volkswagen Golf GTI', 'preco': 239900.0, 'imagem': 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Hatch esportivo que une praticidade, tecnologia e desempenho.', 'motor': '2.0 Turbo', 'potencia': '245 cv', 'velocidade': '250 km/h', 'acessorios': [{'nome': 'Rodas esportivas', 'preco': 7800}, {'nome': 'Kit visual GTI', 'preco': 5200}, {'nome': 'Som premium', 'preco': 3900}], 'imagens_cores': {}, 'categoria': 'Esportivo'}, {'id': 18, 'nome': 'Porsche Cayenne', 'preco': 899900.0, 'imagem': 'https://images.unsplash.com/photo-1614200187524-dc4b892acf16?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV de luxo com desempenho esportivo e amplo espaço interno.', 'motor': '3.0 V6 Turbo', 'potencia': '353 cv', 'velocidade': '248 km/h', 'acessorios': [{'nome': 'Pacote Sport Design', 'preco': 29500}, {'nome': 'Teto panorâmico', 'preco': 16500}, {'nome': 'Interior em couro premium', 'preco': 22500}], 'imagens_cores': {}, 'categoria': 'SUV'}, {'id': 19, 'nome': 'Tesla Model 3', 'preco': 289900.0, 'imagem': 'https://images.unsplash.com/photo-1560958089-b8a1929cee7f?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Sedã elétrico com tecnologia conectada e condução silenciosa.', 'motor': 'Elétrico', 'potencia': '283 cv', 'velocidade': '225 km/h', 'categoria': 'Sedã', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 20, 'nome': 'BYD Seal', 'preco': 299800.0, 'imagem': 'https://images.unsplash.com/photo-1617469767053-d3b523a0b982?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Sedã elétrico com visual esportivo e pacote tecnológico.', 'motor': 'Elétrico', 'potencia': '530 cv', 'velocidade': '180 km/h', 'categoria': 'Sedã', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 21, 'nome': 'BMW iX', 'preco': 699900.0, 'imagem': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV elétrico premium com foco em conforto e conectividade.', 'motor': 'Elétrico', 'potencia': '326 cv', 'velocidade': '200 km/h', 'categoria': 'SUV', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 22, 'nome': 'Mercedes-AMG GT', 'preco': 1250000.0, 'imagem': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Cupê esportivo com engenharia de alto desempenho.', 'motor': '4.0 V8 biturbo', 'potencia': '530 cv', 'velocidade': '312 km/h', 'categoria': 'Esportivo', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 23, 'nome': 'Chevrolet Corvette C8', 'preco': 1190000.0, 'imagem': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Esportivo de motor central e desenho marcante.', 'motor': '6.2 V8', 'potencia': '495 cv', 'velocidade': '296 km/h', 'categoria': 'Esportivo', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 24, 'nome': 'McLaren 720S', 'preco': 3200000.0, 'imagem': 'https://images.unsplash.com/photo-1621135802920-133df287f89c?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Supercarro leve com aerodinâmica avançada.', 'motor': '4.0 V8 biturbo', 'potencia': '720 cv', 'velocidade': '341 km/h', 'categoria': 'Esportivo', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 25, 'nome': 'Audi e-tron GT', 'preco': 649900.0, 'imagem': 'https://images.unsplash.com/photo-1614200187524-dc4b892acf16?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Gran turismo elétrico com interior tecnológico.', 'motor': 'Elétrico', 'potencia': '530 cv', 'velocidade': '245 km/h', 'categoria': 'Elétrico', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 26, 'nome': 'Hyundai Creta Ultimate', 'preco': 179900.0, 'imagem': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV urbano com recursos de conectividade e assistência.', 'motor': '1.0 Turbo', 'potencia': '120 cv', 'velocidade': '185 km/h', 'categoria': 'SUV', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 27, 'nome': 'Volkswagen T-Cross Highline', 'preco': 189900.0, 'imagem': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV compacto versátil para a rotina.', 'motor': '1.4 TSI', 'potencia': '150 cv', 'velocidade': '202 km/h', 'categoria': 'SUV', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 28, 'nome': 'Honda HR-V Touring', 'preco': 195900.0, 'imagem': 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1400&q=85', 'descricao': 'SUV com bom espaço interno e pacote de segurança.', 'motor': '1.5 Turbo', 'potencia': '177 cv', 'velocidade': '200 km/h', 'categoria': 'SUV', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 29, 'nome': 'Fiat Toro Ranch', 'preco': 209900.0, 'imagem': 'https://images.unsplash.com/photo-1551830820-330a71b99659?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Picape versátil com conforto para cidade e estrada.', 'motor': '2.0 Turbo Diesel', 'potencia': '170 cv', 'velocidade': '188 km/h', 'categoria': 'Picape', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}, {'id': 30, 'nome': 'RAM 1500 Laramie', 'preco': 489900.0, 'imagem': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1400&q=85', 'descricao': 'Picape de grande porte com cabine ampla e força.', 'motor': '5.7 V8', 'potencia': '400 cv', 'velocidade': '174 km/h', 'categoria': 'Picape', 'acessorios': [{'nome': 'Pacote de tecnologia', 'preco': 6500}, {'nome': 'Acabamento premium', 'preco': 8200}, {'nome': 'Rodas especiais', 'preco': 9700}], 'imagens_cores': {}}]
CORES = ["Branco", "Preto", "Prata", "Cinza", "Vermelho", "Azul", "Azul-marinho", "Verde", "Verde-escuro", "Amarelo", "Laranja", "Roxo", "Marrom", "Dourado"]
PRECO_CORES = {"Branco":0,"Preto":3500,"Prata":4200,"Cinza":4200,"Vermelho":5800,"Azul":5800,"Azul-marinho":5800,"Verde":6500,"Verde-escuro":6500,"Amarelo":7200,"Laranja":7200,"Roxo":7200,"Marrom":5200,"Dourado":8500}

def conectar_banco():
    conexao=sqlite3.connect(BANCO); conexao.row_factory=sqlite3.Row; return conexao

def criar_banco():
    with conectar_banco() as c:
        c.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT NOT NULL,email TEXT NOT NULL UNIQUE,senha TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS configuracoes (id INTEGER PRIMARY KEY AUTOINCREMENT,usuario_id INTEGER NOT NULL,carro_id INTEGER NOT NULL,cor TEXT NOT NULL,acessorios TEXT,total REAL NOT NULL,criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(usuario_id) REFERENCES usuarios(id))")
        c.execute("""CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            carro_id INTEGER NOT NULL,
            cor TEXT NOT NULL,
            acessorios TEXT,
            total REAL NOT NULL,
            nome_destinatario TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL,
            cep TEXT NOT NULL,
            endereco TEXT NOT NULL,
            numero TEXT NOT NULL,
            complemento TEXT,
            bairro TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            observacoes TEXT,
            status TEXT NOT NULL DEFAULT 'Aguardando contato',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )""")

def usuario_logado(): return session.get("usuario_id") is not None

def moeda(valor): return f"R$ {valor:,.2f}".replace(",","X").replace(".",",").replace("X",".")

@app.context_processor
def dados_globais(): return {"usuario_nome":session.get("usuario_nome"),"moeda":moeda}

@app.route("/")
def index():
    if not usuario_logado(): return redirect(url_for("login"))
    categorias=sorted({c['categoria'] for c in CARROS})
    return render_template("index.html",carros=CARROS,categorias=categorias)

@app.route("/login",methods=["GET","POST"])
def login():
    if usuario_logado(): return redirect(url_for("index"))
    if request.method=="POST":
        email=request.form.get("email","").strip().lower(); senha=request.form.get("senha","")
        with conectar_banco() as c: usuario=c.execute("SELECT * FROM usuarios WHERE email=?",(email,)).fetchone()
        if usuario and check_password_hash(usuario['senha'],senha):
            session.clear(); session['usuario_id']=usuario['id']; session['usuario_nome']=usuario['nome']; flash("Bem-vindo de volta!","sucesso"); return redirect(url_for("index"))
        flash("E-mail ou senha incorretos.","erro")
    return render_template("login.html")

@app.route("/cadastro",methods=["GET","POST"])
def cadastro():
    if usuario_logado(): return redirect(url_for("index"))
    if request.method=="POST":
        nome=request.form.get("nome","").strip(); email=request.form.get("email","").strip().lower(); senha=request.form.get("senha",""); confirmar=request.form.get("confirmar_senha","")
        if not nome or not email or not senha: flash("Preencha todos os campos.","erro")
        elif len(senha)<6: flash("A senha precisa ter pelo menos 6 caracteres.","erro")
        elif senha!=confirmar: flash("As senhas não coincidem.","erro")
        else:
            try:
                with conectar_banco() as c: c.execute("INSERT INTO usuarios(nome,email,senha) VALUES(?,?,?)",(nome,email,generate_password_hash(senha)))
                flash("Conta criada! Agora entre com seus dados.","sucesso"); return redirect(url_for("login"))
            except sqlite3.IntegrityError: flash("Este e-mail já está cadastrado.","erro")
    return render_template("cadastro.html")

@app.route("/carro/<int:carro_id>",methods=["GET","POST"])
def detalhes(carro_id):
    if not usuario_logado(): return redirect(url_for("login"))
    carro=next((x for x in CARROS if x['id']==carro_id),None)
    if carro is None: flash("Veículo não encontrado.","erro"); return redirect(url_for("index"))
    if request.method=="POST":
        cor=request.form.get("cor","Branco")
        if cor not in CORES: cor="Branco"
        escolhidos=set(request.form.getlist("acessorios"))
        validos=[a for a in carro['acessorios'] if a['nome'] in escolhidos]
        subtotal=sum(float(a['preco']) for a in validos); extra=float(PRECO_CORES[cor]); total=round(float(carro['preco'])+subtotal+extra,2)
        with conectar_banco() as c: c.execute("INSERT INTO configuracoes(usuario_id,carro_id,cor,acessorios,total) VALUES(?,?,?,?,?)",(session['usuario_id'],carro_id,cor,", ".join(a['nome'] for a in validos),total))
        return render_template("interesse.html",carro=carro,cor=cor,acessorios=validos,preco_cor=extra,subtotal_acessorios=subtotal,total=total)
    return render_template("carro.html",carro=carro,cores=CORES,preco_cores=PRECO_CORES)

@app.route("/finalizar-entrega", methods=["POST"])
def finalizar_entrega():
    if not usuario_logado():
        return redirect(url_for("login"))
    carro_id = request.form.get("carro_id", type=int)
    carro = next((x for x in CARROS if x["id"] == carro_id), None)
    if carro is None:
        flash("Veículo não encontrado. Selecione novamente.", "erro")
        return redirect(url_for("index"))

    campos = {
        "nome_destinatario": request.form.get("nome_destinatario", "").strip(),
        "telefone": request.form.get("telefone", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "cep": request.form.get("cep", "").strip(),
        "endereco": request.form.get("endereco", "").strip(),
        "numero": request.form.get("numero", "").strip(),
        "complemento": request.form.get("complemento", "").strip(),
        "bairro": request.form.get("bairro", "").strip(),
        "cidade": request.form.get("cidade", "").strip(),
        "estado": request.form.get("estado", "").strip().upper(),
        "observacoes": request.form.get("observacoes", "").strip(),
    }
    obrigatorios = ["nome_destinatario", "telefone", "email", "cep", "endereco", "numero", "bairro", "cidade", "estado"]
    if any(not campos[k] for k in obrigatorios):
        flash("Preencha todos os campos obrigatórios para a entrega.", "erro")
        return redirect(url_for("detalhes", carro_id=carro_id))

    cor = request.form.get("cor", "Branco")
    if cor not in CORES:
        cor = "Branco"
    selecionados = set(request.form.getlist("acessorios"))
    validos = [a for a in carro["acessorios"] if a["nome"] in selecionados]
    subtotal = sum(float(a["preco"]) for a in validos)
    extra = float(PRECO_CORES[cor])
    total = round(float(carro["preco"]) + subtotal + extra, 2)
    nomes = ", ".join(a["nome"] for a in validos)
    with conectar_banco() as c:
        cur = c.execute("""INSERT INTO pedidos
            (usuario_id,carro_id,cor,acessorios,total,nome_destinatario,telefone,email,cep,endereco,numero,complemento,bairro,cidade,estado,observacoes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (session["usuario_id"],carro_id,cor,nomes,total,campos["nome_destinatario"],campos["telefone"],campos["email"],campos["cep"],campos["endereco"],campos["numero"],campos["complemento"],campos["bairro"],campos["cidade"],campos["estado"],campos["observacoes"]))
        pedido_id = cur.lastrowid
    return render_template("pedido_confirmado.html", carro=carro, cor=cor, acessorios=validos, total=total, pedido_id=pedido_id, entrega=campos)

@app.route("/sair")
def sair(): session.clear(); flash("Você saiu da sua conta.","sucesso"); return redirect(url_for("login"))

@app.errorhandler(404)
def nao_encontrado(_): return render_template("404.html"),404

if __name__=="__main__":
    criar_banco(); app.run(debug=True)
