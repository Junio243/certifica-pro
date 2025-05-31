# SECURITY AUDIT – CertificaPro Clone

Este documento lista melhorias de segurança implementadas em relação ao protótipo da Manus.

- Removido `certificados.json` da pasta pública
- Painel admin com Flask‑Login, sessão protegida e CSRF via WTForms
- Credenciais armazenadas em variáveis de ambiente (.env)
- Cabeçalhos seguros adicionados via ProxyFix (não incluído nesta demo, mas já preparado)
