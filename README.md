# 📘 FlowMind AI — Inteligência Artificial para Saúde Mental

API em Python + FastAPI que pega os check-ins diários do usuário, entende o que está acontecendo com humor, sono e energia, e devolve relatórios bem escritos e previsões realistas de burnout. 

## 🚀 Tecnologias Utilizadas

- Python 3.12
- FastAPI + Uvicorn
- OpenAI (GPT-4o / GPT-4 turbo)
- TensorFlow / Keras
- Firebase Admin SDK (Firestore)
- Pydantic v2
- python-dotenv

## 🧠 Funcionalidades

**Relatórios que parecem escritos por gente**  
A partir dos check-ins e rotinas, gera um texto fluido, pessoal, com análise de tendências e sugestões que realmente fazem sentido.

**Previsão de burnout que funciona**  
Modelo de rede neural treinado com dados reais que entrega um score de 0 a 1, classifica o risco (Baixo/Médio/Alto/Crítico), explica o motivo e já sugere o que fazer pra não quebrar.

**Tudo salvo automaticamente**  
Cada relatório e cada previsão vai direto pro Firestore:

```
insights/{user_id}/
├── relatorios/{timestamp}.json
└── burnout/{timestamp}.json
```

## 📡 Endpoints

| Método | Endpoint                | O que faz                              |
|--------|-------------------------|----------------------------------------|
| GET    | `/`                     | Confirma que a API tá viva             |
| POST   | `/relatorio/{user_id}`  | Gera o relatório completo              |
| POST   | `/burnout/{user_id}`    | Roda a predição de burnout             |

Docs interativas → http://localhost:8000/docs

### Resposta do relatório
```json
{
  "relatorio": "Essa semana seu sono tá redondo (7h30 em média), mas a energia despenca depois das 16h e o humor tá mais instável desde quarta...",
  "periodo": "10/11 a 20/11",
  "timestamp": "2025-11-21T14:22:00Z"
}
```

### Resposta do burnout 
```json
{
  "score": 0.78,
  "nivel": "Alto",
  "justificativa": "Energia em queda livre + humor baixo em 8 dos últimos 10 dias",
  "recomendacoes": [
    "Parar de trabalhar depois das 18h",
    "Colocar pausa de 10 min a cada 90 min",
    "Dormir antes das 23h30 pelo menos 4x na semana"
  ]
}
```

## 🔧 Como rodar localmente

```bash
git clone https://github.com/seu-user/flowmind-ia.git
cd flowmind-ia

python -m venv venv
source venv/bin/activate    # mac/linux
# venv\Scripts\activate     # windows

pip install -r requirements.txt

# .env
echo "OPENAI_API_KEY=sua-chave-aqui" > .env

# joga a chave do firebase em
./firebase/firebase-key.json

uvicorn app:app --reload
```

→ http://127.0.0.1:8000

## 📂 Estrutura

```
flowmind_ia/
├── app.py
├── requirements.txt
├── .env
├── firebase/firebase-key.json
└── services/
    ├── firestore_service.py
    ├── openai_service.py
    └── burnout_model.py
