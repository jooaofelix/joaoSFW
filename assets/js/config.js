/*
 * Configuração da Desata
 * ----------------------
 * Todos os dados que mudam com frequência (contato, textos curtos de CTA)
 * ficam centralizados aqui. Edite este arquivo, não o HTML.
 *
 * Se um campo obrigatório ficar vazio, o site mostra um aviso de configuração
 * na seção de contato, em vez de um botão que não abre conversa nenhuma.
 *
 * O gerar-convite.py lê este mesmo arquivo: editar aqui muda o site e o
 * convite em PDF.
 */
window.DESATA_CONFIG = {
  // Número do WhatsApp com código do país e DDD, só dígitos.
  whatsapp: "5512991338866",

  // Mensagem que já vem escrita quando a pessoa abre o WhatsApp.
  whatsappMensagem:
    "Olá! Vim pelo site da Desata e quero conversar sobre um projeto.",

  // E-mail de contato.
  email: "jvctrfelix@gmail.com",

  // PENDENTE (opcional): perfil do Instagram, só o usuário, sem "@".
  instagram: "",

  // Cidade/região de atuação, exibida no rodapé.
  local: "São José dos Campos · SP"
};
