AUTOPRIME — EDIÇÃO TECH

O projeto foi atualizado com identidade visual tecnológica em azul profundo, ciano e violeta, catálogo expandido e interações novas.

CONTEÚDO
- app.py: aplicação Flask e catálogo com 30 veículos.
- autoprime.db: cópia do banco enviado, preservando usuários e configurações existentes.
- templates/: login, cadastro, catálogo, configurador, confirmação e 404.
- static/css/: layout responsivo e tema visual tecnológico.
- static/js/: busca, filtros, ordenação, favoritos e cálculo dinâmico do configurador.

INSTALAÇÃO NO WINDOWS
1. Extraia o ZIP para uma pasta.
2. Abra o terminal dentro da pasta extraída.
3. Execute: py -m pip install -r requirements.txt
4. Execute: py app.py
5. Acesse http://127.0.0.1:5000

RECURSOS
- 30 modelos, divididos por categoria.
- Busca instantânea por nome, filtros por categoria e ordenação por preço/nome.
- Favoritos salvos no navegador.
- Página individual para cada veículo.
- Configuração de pintura e acessórios com preço atualizado imediatamente.
- O servidor recalcula o preço ao receber o formulário; valores enviados pelo navegador não são considerados confiáveis.
- Interface adaptada para desktop e celular.

IMPORTANTE
- As imagens são carregadas de fontes externas e exigem internet. Algumas imagens são ilustrativas e podem não corresponder exatamente ao modelo indicado.
- A simulação de pintura usa filtros na mesma foto, não representa uma fotografia real do veículo em cada cor.
- A aplicação salva configurações, mas não realiza pagamentos nem conclui compras.
- Antes de publicar na internet, troque SECRET_KEY por uma chave forte, desative debug e configure HTTPS.
- O banco incluído é uma cópia do banco enviado nesta conversa. Guarde uma cópia segura antes de substituir qualquer banco local.
