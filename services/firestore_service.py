import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreClient:

    def __init__(self):
        # caminho relativo: firebase/firebase-key.json
        key_path = os.path.join("firebase", "firebase-key.json")

        if not os.path.exists(key_path):
            raise FileNotFoundError(
                f"Arquivo de credenciais não encontrado em: {key_path}"
            )

        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    # ---------- LEITURA DE DADOS ----------

    def get_checkins(self, user_id: str):
        docs = (
            self.db.collection("checkins")
            .document(user_id)
            .collection("registros")
            .stream()
        )
        return [d.to_dict() for d in docs]

    def get_rotinas(self, user_id: str):
        docs = (
            self.db.collection("rotinas")
            .document(user_id)
            .collection("dias")
            .stream()
        )
        return [d.to_dict() for d in docs]

    # ---------- SALVAR INSIGHTS (RELATÓRIO / BURNOUT) ----------

    def salvar_insight(self, user_id: str, tipo: str, payload: dict):
        """
        Salva um insight no Firestore em:
        insights/{user_id}/{tipo}/{timestamp}
        Ex.: tipo = "relatorio" ou "burnout"
        """
        timestamp = datetime.utcnow().isoformat()

        (
            self.db.collection("insights")
            .document(user_id)
            .collection(tipo)
            .document(timestamp)
            .set(payload)
        )
