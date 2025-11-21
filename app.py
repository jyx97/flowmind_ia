from fastapi import FastAPI, HTTPException

from services.firestore_service import FirestoreClient
from services.ia_service import gerar_relatorio
from services.burnout_service import BurnoutNeuralService

app = FastAPI(title="FlowMind IA")

db = FirestoreClient()
burnout_service = BurnoutNeuralService()


@app.get("/")
def root():
    return {"status": "FlowMind IA rodando"}

@app.post("/relatorio/{user_id}")
def gerar_relatorio_endpoint(user_id: str):

    checkins = db.get_checkins(user_id)
    rotinas = db.get_rotinas(user_id)

    if not checkins and not rotinas:
        raise HTTPException(
            status_code=404,
            detail="Nenhum dado de check-in ou rotina encontrado para este usuário.",
        )

    texto = gerar_relatorio(checkins, rotinas)

    payload = {
        "usuario": user_id,
        "tipo": "relatorio_emocional",
        "texto": texto,
        "checkins_usados": checkins,
        "rotinas_usadas": rotinas,
    }

    db.salvar_insight(user_id, "relatorio", payload)

    return payload



@app.post("/burnout/{user_id}")
def gerar_burnout_endpoint(user_id: str):
    """
    Usa rede neural em Python (TensorFlow) para estimar
    risco de burnout baseado nos check-ins do usuário.
    Também salva o resultado no Firestore.
    """

    checkins = db.get_checkins(user_id)

    if not checkins:
        raise HTTPException(
            status_code=404,
            detail="Nenhum check-in encontrado para este usuário.",
        )

    resultado = burnout_service.analisar_risco(checkins)

    payload = {
        "usuario": user_id,
        "tipo": "risco_burnout",
        "risco_percentual": resultado["risco_percentual"],
        "nivel": resultado["nivel"],
        "detalhes": resultado["detalhes"],
        "checkins_usados": checkins,
    }

    # 💾 salvar insight no Firestore
    db.salvar_insight(user_id, "burnout", payload)

    return payload
