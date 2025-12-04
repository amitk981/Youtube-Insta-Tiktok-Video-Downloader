const TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const MONETAG_LINK = "https://otieu.com/4/10256428";

exports.handler = async (event, context) => {
    console.log(`Received ${event.httpMethod} request`);

    // Health check
    if (event.httpMethod === 'GET') {
        return {
            statusCode: 200,
            body: JSON.stringify({
                status: 'Bot is running',
                token_set: !!TOKEN
            })
        };
    }

    // Webhook handler
    if (event.httpMethod === 'POST') {
        try {
            if (!TOKEN) {
                console.error('TELEGRAM_BOT_TOKEN not set');
                return {
                    statusCode: 500,
                    body: 'Token missing'
                };
            }

            const update = JSON.parse(event.body);
            console.log('Received update:', JSON.stringify(update).substring(0, 200));

            // Handle /start command
            if (update.message && update.message.text === '/start') {
                const chatId = update.message.chat.id;

                // Send message with Monetag link
                const response = await fetch(`https://api.telegram.org/bot${TOKEN}/sendMessage`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        chat_id: chatId,
                        text: '🎬 Welcome to Video Downloader Bot!\n\nTo use this bot, please verify you are human by clicking the link below:',
                        reply_markup: {
                            inline_keyboard: [[
                                { text: '🎁 Click here to access bot', url: MONETAG_LINK }
                            ]]
                        }
                    })
                });

                const result = await response.json();
                console.log('Sent message:', result.ok ? 'success' : 'failed');
            }

            return {
                statusCode: 200,
                body: 'OK'
            };

        } catch (error) {
            console.error('Error:', error);
            return {
                statusCode: 500,
                body: error.message
            };
        }
    }

    return {
        statusCode: 405,
        body: 'Method not allowed'
    };
};
