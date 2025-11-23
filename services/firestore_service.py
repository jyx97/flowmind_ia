import base64
import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreClient:

    def __init__(self):
        # caminho relativo: firebase/firebase-key.json
        base64_key = os.getenv("FIREBASE_KEY_BASE64")
        if base64_key:
            # --- Rodando no Railway ---
            decoded = base64.b64decode(base64_key).decode("utf-8")
            service_account_info = json.loads(decoded)
            cred = credentials.Certificate(service_account_info)

            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)

        else:
            # --- Rodando localmente, com arquivo físico ---
            key_path = os.path.join("firebase", "firebase-key.json")
            if not os.path.exists(key_path):
                raise FileNotFoundError(
                    f"Credenciais não encontradas.\n"
                    f"Tente setar FIREBASE_KEY_BASE64 no Railway ou coloque o arquivo local em: {key_path}"
                )

            cred = credentials.Certificate(key_path)

            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    # le dados

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

    # salva dados

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
