# Approxima Chatbot (Telegram)

Chatbot de Telegram que será desenvolvido como MVP (Minimum Valueable Product) da iniciativa Approxima

## Acabou de clonar o repositório?

Rode o comando `pip install -r requirements.txt` para instalar as libs necessárias.

## Lista de comandos (@approxima_bot)

- /start => Inicia o bot. Se a pessoa não estiver cadastrada na base de dados (dá pra ver pelo ID da conversa/Tele [ver qual é melhor]), pede para ela fornecer um nome, uma pequena descrição pessoal e sugere a ela escolher seus primeiros interesses.

- /prefs => Retorna lista de interesses (caixa de seleção). A pessoa pode marcar ou desmarcar o que ela quiser.

- /show => Mostra uma pessoa que tem interesses em comum (vai com base no ranking). Embaixo, um botão para enviar a solicitação de conexão deve existir.

- /random => Mostra uma pessoa aleatória. Embaixo, um botão para enviar a solicitação de conexão deve existir.

- /clear => Permite que as pessoas que o usuário respondeu com "Agora não" apareçam de novo nas sugestões delu (quando elu responde com "Agora não", aquele usuário vai para o campo de "rejeitados", então não irá aparecer como sugestão novamente AO MENOS que ele dê esse comando).

- [IDEIA / FEATURE ADICIONAL] /opposite => Mostra uma pessoa que tem interesses opostos (vai com base no ranking reverso). Embaixo, um botão para enviar a solicitação de conexão deve existir.

- /pending => Mostra todas as solicitações de conexão que aquela pessoa possui e para as quais ela ainda não deu uma resposta. Mostra, para cada solicitação, a descrição da pessoa e dois botões: conectar ou descartar).

- /friends => Mostra o contato (@ do Tele) de todas as pessoas com que o usuário já se conectou.

- /help => Mostra os comandos disponíveis.
