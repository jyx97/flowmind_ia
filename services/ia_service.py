from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_relatorio(checkins, rotinas):
    
    texto_checkins = ""
    for c in checkins:
        texto_checkins += (
            f"- Dia {c.get('dataCheckin', '?')}: "
            f"Humor {c.get('humor', '?')}, "
            f"Energia {c.get('energia', '?')}, "
            f"Sono {c.get('sono', '?')}\n"
        )

    texto_rotinas = ""
    for r in rotinas:
        texto_rotinas += (
            f"- Dia {r.get('dataRotina', '?')}: "
            f"{r.get('rotinaJson', '')[:200]}...\n"
        )

    prompt = f"""
    Você é um assistente especializado em saúde mental, produtividade e burnout.

    Abaixo estão dados de um usuário:

    CHECK-INS (humor, energia, sono):
    {texto_checkins}

    ROTINAS GERADAS PELA IA:
    {texto_rotinas}

    Com base nesses dados, gere um RELATÓRIO organizado com os tópicos:

    1) RESUMO GERAL DO ESTADO EMOCIONAL
    2) PADRÕES OBSERVADOS (humor, energia, sono)
    3) POSSÍVEIS SINAIS DE ESTRESSE OU BURNOUT
    4) FATORES POSITIVOS (o que está ajudando)
    5) RECOMENDAÇÕES PRÁTICAS PARA OS PRÓXIMOS 7 DIAS

    Use linguagem acolhedora, objetiva e em português.
    """

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return resposta.choices[0].message.content
