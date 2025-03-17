const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');

const app = express();
app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', qr => {
    console.log('Escaneie o QR Code abaixo para logar:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Cliente WhatsApp pronto!');
    // Aqui você pode enviar uma mensagem de teste se desejar
    // const number = '5511999999999';
    // const message = 'Mensagem de teste!';
    // client.sendMessage(`${number}@c.us`, message)
    //     .then(response => console.log('Mensagem de teste enviada:', response))
    //     .catch(error => console.log('Erro no envio de mensagem de teste:', error));
});

client.initialize();

app.post('/send', async (req, res) => {
    const { number, message } = req.body;
    console.log('Número recebido:', number);  // Verifique os dados recebidos
    console.log('Mensagem recebida:', message);  // Verifique os dados recebidos
    try {
        const formattedNumber = number.includes('@c.us') ? number : `${number}@c.us`;
        await client.sendMessage(formattedNumber, message);
        res.json({ success: true, message: 'Mensagem enviada!' });
    } catch (error) {
        console.error('Erro ao enviar a mensagem:', error);  // Log completo do erro
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(3000, () => console.log('Servidor rodando na porta 3000'));
