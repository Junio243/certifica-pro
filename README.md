# CertificaPro – Sistema de Validação de Certificados

## Como rodar localmente

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # depois edite a chave secreta e credenciais
python app.py
```

## Deploy no Render

- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`

## Firebase Firestore

- Crie um projeto Firebase, habilite Firestore.
- Gere Service Account JSON e salve como `firebase_key.json` na raiz.
