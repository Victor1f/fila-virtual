from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random

app = FastAPI()

# --- DADOS SALVOS NA MEMÓRIA DO SERVIDOR ---
fila_da_loja = []
contador_id = 1
tempo_medio = 15 # Tempo de espera inicial da cantina (15 min)

adjetivos = ["Leão", "Raposa", "Urso", "Falcão", "Tigre", "Lobo"]
caracteristicas = ["Corajoso", "Veloz", "Sábio", "Atento", "Forte", "Ágil"]

class TempoUpdate(BaseModel):
    tempo: int

# --- ROTAS PARA ENTREGAR AS PÁGINAS E IMAGENS ---
@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/fila.html")
def pagina_fila():
    return FileResponse("fila.html")

@app.get("/admin.html")
def pagina_admin():
    return FileResponse("admin.html")

@app.get("/logo.jpeg")
def logo_principal():
    return FileResponse("logo.jpeg")

@app.get("/logo-ueg.png")
def logo_cantina():
    return FileResponse("logo-ueg.png")

# --- ROTAS DA API (COMUNICAÇÃO DE DADOS) ---
@app.get("/api/status")
def ver_status():
    return {
        "fila": fila_da_loja,
        "total_pessoas": len(fila_da_loja),
        "tempo_medio": tempo_medio
    }

@app.post("/api/entrar")
def entrar_na_fila():
    global contador_id
    nome_aleatorio = random.choice(adjetivos) + " " + random.choice(caracteristicas)
    
    novo_cliente = {"id": contador_id, "nome": nome_aleatorio}
    fila_da_loja.append(novo_cliente)
    contador_id += 1 
    
    return novo_cliente

@app.post("/api/chamar")
def chamar_proximo():
    if len(fila_da_loja) > 0:
        chamado = fila_da_loja.pop(0)
        return {"mensagem": "Sucesso", "chamado": chamado}
    
    return {"mensagem": "Fila vazia"}

@app.post("/api/tempo")
def atualizar_tempo(dados: TempoUpdate):
    global tempo_medio
    tempo_medio = dados.tempo
    return {"mensagem": "Tempo atualizado com sucesso"}
