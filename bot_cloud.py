"""
Bot Telegram para consultar torneios do Bodog - VERSÃO CLOUD
Roda 24/7 na nuvem sem precisar do PC ligado
"""

import os
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token do bot (NÃO COMPARTILHE!)
BOT_TOKEN = "8356133755:AAHfKvHCrDyDxL72ej1QBVhit0kr3KdndWc"

# Lista de torneios (EDITE AQUI se mudar horário/valor)
TORNEIOS = [
    ("4.777 GTD (Lucky)", "05:23", "$27,50"),
    ("1.000 GTD (Monster)", "05:27", "$7,70"),
    ("1.000 GTD (Omaha H/L)", "06:30", "$11,00"),
    ("2.999 GTD (Niner)", "07:15", "$22,00"),
    ("1.212 GTD (Dozens)", "07:32", "$13,20"),
    ("5.888 GTD (Crazy)", "14:33", "$16,50"),
    ("1.999 GTD (Niner)", "15:40", "$9,90"),
    ("2.500 GTD (Monster)", "15:49", "$22,00"),
    ("5.888 GTD (Crazy)", "17:31", "$16,50"),
    ("6.888 GTD (Crazy)", "17:32", "$11,00"),
    ("4.000 GTD (10K Fichas)", "19:01", "$33,00"),
    ("1.000 GTD (Omaha H/L)", "19:39", "$11,00"),
    ("3.999 GTD (Niner)", "19:40", "$16,50"),
    ("5.888 GTD (Crazy)", "20:11", "$16,50"),
    ("2.000 GTD (Monster)", "20:24", "$11,00"),
    ("5.000 GTD (10K Fichas)", "21:30", "$33,00"),
    ("6.000 GTD (Roller)", "22:36", "$16,50"),
    ("2.888 GTD (KO)", "23:11", "$11,00"),
    ("1.500 GTD (Roller)", "23:35", "$5,50"),
    ("2.888 GTD (Omaha H/L)", "00:10", "$22,00"),
    ("4.777 GTD (Lucky)", "00:23", "$11,00"),
    ("777 GTD (Omaha H/L)", "00:30", "$7,70"),
    ("10.000 GTD (Monster)", "00:39", "$27,50"),
    ("1.000 GTD (Monster)", "01:08", "$4,40"),
    ("750 GTD (Nightly)", "01:52", "$5,50"),
    ("12.888 GTD (Crazy)", "02:11", "$16,50"),
    ("35.000 GTD (Nightly)", "02:32", "$55,00"),
    ("5.999 GTD (Niner)", "03:40", "$9,90"),
    ("4.999 GTD (Omaha H/L)", "03:45", "$33,00"),
]

def filtrar_proximos(horas=None):
    """Filtra torneios futuros"""
    agora = datetime.now()
    hora_atual = agora.hour * 60 + agora.minute
    HORARIO_RESET = 6
    
    torneios_futuros = []
    for nome, horario, buyin in TORNEIOS:
        try:
            hora, minuto = map(int, horario.split(':'))
            horario_minutos = hora * 60 + minuto
            diff_minutos = horario_minutos - hora_atual
            
            if diff_minutos < 0:
                if hora < HORARIO_RESET:
                    diff_minutos = (24 * 60 - hora_atual) + horario_minutos
                else:
                    continue
            
            if horas:
                if diff_minutos <= (horas * 60):
                    torneios_futuros.append((nome, horario, buyin))
            else:
                torneios_futuros.append((nome, horario, buyin))
        except:
            continue
    
    return torneios_futuros

def formatar_mensagem(torneios, titulo):
    """Formata lista de torneios"""
    if not torneios:
        return f"<b>{titulo}</b>\n\n❌ Nenhum torneio encontrado."
    
    msg = f"<b>{titulo}</b>\n"
    msg += f"📊 Total: {len(torneios)} torneio(s)\n\n"
    
    for nome, horario, buyin in torneios:
        msg += f"⏳ <b>{horario}</b> - {nome}\n"
        msg += f"   💰 Buy-in: {buyin}\n\n"
    
    return msg

def criar_teclado():
    """Cria teclado personalizado"""
    keyboard = [
        [KeyboardButton("📋 Lista Completa"), KeyboardButton("⏭️ Próximos")],
        [KeyboardButton("⏰ Próxima 1h"), KeyboardButton("⏰ Próximas 2h")],
        [KeyboardButton("⏰ Próximas 3h"), KeyboardButton("❓ Ajuda")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    msg = """
🎰 <b>Bot de Torneios Bodog</b>

Bem-vindo! Use os botões abaixo para consultar os torneios.

📋 <b>Lista Completa</b> - Todos os 29 torneios
⏭️ <b>Próximos</b> - Torneios que ainda vão começar
⏰ <b>Próxima 1h/2h/3h</b> - Filtro por tempo

<i>🌐 Bot rodando 24/7 na nuvem!</i>
"""
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=criar_teclado())

async def cmd_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista completa"""
    msg = formatar_mensagem(TORNEIOS, "📋 Todos os Torneios Agendados")
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=criar_teclado())

async def cmd_proximos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Próximos torneios"""
    torneios = filtrar_proximos()
    msg = formatar_mensagem(torneios, "⏭️ Próximos Torneios")
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=criar_teclado())

async def cmd_proxima1h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Próxima 1 hora"""
    torneios = filtrar_proximos(horas=1)
    msg = formatar_mensagem(torneios, "⏰ Torneios na Próxima 1 Hora")
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=criar_teclado())

async def cmd_proximas2h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Próximas 2 horas"""
    torneios = filtrar_proximos(horas=2)
    msg = formatar_mensagem(torneios, "⏰ Torneios nas Próximas 2 Horas")
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=criar_teclado())

async def cmd_proximas3h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Próximas 3 horas"""
    torneios = filtrar_proximos(horas=3)
    msg = formatar_mensagem(torneios, "⏰ Torneios nas Próximas 3 Horas")
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=criar_teclado())

async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa botões"""
    texto = update.message.text
    
    if texto == "📋 Lista Completa":
        await cmd_lista(update, context)
    elif texto == "⏭️ Próximos":
        await cmd_proximos(update, context)
    elif texto == "⏰ Próxima 1h":
        await cmd_proxima1h(update, context)
    elif texto == "⏰ Próximas 2h":
        await cmd_proximas2h(update, context)
    elif texto == "⏰ Próximas 3h":
        await cmd_proximas3h(update, context)
    elif texto == "❓ Ajuda":
        await cmd_start(update, context)

def main():
    """Inicia o bot"""
    print("🤖 Bot Telegram iniciando na nuvem...")
    print(f"📋 Torneios: {len(TORNEIOS)}")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Registra comandos
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler(["ajuda", "help"], cmd_start))
    app.add_handler(CommandHandler("lista", cmd_lista))
    app.add_handler(CommandHandler(["proximos", "prox"], cmd_proximos))
    app.add_handler(CommandHandler(["proxima1h", "1h"], cmd_proxima1h))
    app.add_handler(CommandHandler(["proximas2h", "2h"], cmd_proximas2h))
    app.add_handler(CommandHandler(["proximas3h", "3h"], cmd_proximas3h))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_mensagem))
    
    print("✅ Bot rodando 24/7!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
