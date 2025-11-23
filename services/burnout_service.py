import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class BurnoutNeuralService:

    def __init__(self):
        self.model = Sequential(
            [
                Dense(16, activation="relu", input_shape=(5,)),
                Dense(8, activation="relu"),
                Dense(1, activation="sigmoid"),  # saída: risco 0–1
            ]
        )
        self.model.compile(optimizer="adam", loss="mse")

    def _extrair_features(self, checkins):

        if not checkins:
            return None

        humores = np.array(
            [c.get("humor", 0) for c in checkins], dtype=float
        )
        energias = np.array(
            [c.get("energia", 0) for c in checkins], dtype=float
        )
        sonos = np.array(
            [c.get("sono", 0) for c in checkins], dtype=float
        )

        media_humor = humores.mean()
        media_energia = energias.mean()
        media_sono = sonos.mean()

        tendencia_humor = humores[-1] - humores[0]
        tendencia_energia = energias[-1] - energias[0]

        sono_ruim_ratio = float((sonos < 6).sum()) / len(sonos)

        features = np.array(
            [
                media_humor,
                media_energia,
                media_sono,
                tendencia_humor,
                sono_ruim_ratio,
            ],
            dtype=float,
        )

        return features

    def _heuristica_risco(self, features):
        media_humor, media_energia, media_sono, tendencia_humor, sono_ruim_ratio = features

        risco = 0.1

        if media_humor < 5:
            risco += 0.2
        if media_energia < 5:
            risco += 0.2
        if media_sono < 6:
            risco += 0.2
        if tendencia_humor < -1:
            risco += 0.15
        if sono_ruim_ratio > 0.4:
            risco += 0.25

        risco = max(0.0, min(1.0, risco))
        return risco

    def _treinar_modelo_personalizado(self, features):
        risco_base = self._heuristica_risco(features)

        X = []
        y = []

        for _ in range(64):
            ruido = np.random.normal(0, 0.3, size=features.shape)
            f_ruido = features + ruido
            X.append(f_ruido)

            y_val = risco_base + np.random.normal(0, 0.05)
            y_val = max(0.0, min(1.0, y_val))
            y.append(y_val)

        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)

        self.model.fit(X, y, epochs=40, verbose=0)

    def analisar_risco(self, checkins):
        if len(checkins) < 4:
            return {
                "risco_percentual": 10,
                "nivel": "baixo",
                "detalhes": [
                    "Poucos dados de check-in; risco estimado baixo por falta de histórico suficiente."
                ],
            }

        features = self._extrair_features(checkins)
        if features is None:
            return {
                "risco_percentual": 10,
                "nivel": "baixo",
                "detalhes": [
                    "Não foi possível extrair dados de check-in."
                ],
            }

        self._treinar_modelo_personalizado(features)

        X_input = features.reshape(1, -1)
        risco_modelo = float(
            self.model.predict(X_input, verbose=0)[0][0]
        )

        risco_percentual = int(risco_modelo * 100)

        if risco_percentual < 30:
            nivel = "baixo"
        elif risco_percentual < 60:
            nivel = "moderado"
        else:
            nivel = "alto"

        detalhes = []

        media_humor, media_energia, media_sono, tendencia_humor, sono_ruim_ratio = features

        if media_humor < 5:
            detalhes.append("Humor médio abaixo do ideal.")
        if media_energia < 5:
            detalhes.append("Energia média baixa.")
        if media_sono < 6:
            detalhes.append("Sono médio reduzido.")
        if tendencia_humor < -1:
            detalhes.append(
                "Tendência de queda no humor ao longo dos dias."
            )
        if sono_ruim_ratio > 0.4:
            detalhes.append(
                "Muitas noites com pouco sono (< 6h)."
            )

        if not detalhes:
            detalhes.append(
                "Sem fatores críticos fortes, mas é importante manter hábitos saudáveis."
            )

        return {
            "risco_percentual": risco_percentual,
            "nivel": nivel,
            "detalhes": detalhes,
        }
