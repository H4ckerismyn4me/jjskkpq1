import random
import string
import telebot

bot = telebot.TeleBot('6047420488:AAHUYMbfeHYhkyHIqPUHgcpJUnMrC_OJLa0')
prefixes = ['/', '.', '!']

@bot.message_handler(func=lambda message: message.text.startswith(tuple(prefixes)) and message.text[1:].startswith('gen'))
def generar_tarjetas(message):
    try:
        mensaje = message.text.split()
        bin = mensaje[1]
        if len(bin) < 6:
            raise Exception("El BIN debe tener al menos 6 dígitos")


        # Generar las tarjetas
        tarjetas_generadas = []
        for i in range(10):
            # Generar el dígito que reemplazará a "x"
            digitos_bin = list(bin)
            for j in range(len(digitos_bin)):
                if digitos_bin[j] == "x":
                    digitos_bin[j] = str(random.randint(0, 9))
            bin_completo = "".join(digitos_bin)

            # Validar el número generado con el algoritmo de Luhn
            digitos_faltantes = 16 - len(bin_completo)
            for k in range(1000):
                digitos_aleatorios = ''.join(random.choice(string.digits) for _ in range(digitos_faltantes - 1))
                tarjeta = bin_completo + digitos_aleatorios[:16-len(bin_completo)]
                suma = 0
                for j, digito in enumerate(tarjeta[::-1]):
                    valor = int(digito)
                    if j % 2 == 0:
                        valor *= 2
                        if valor > 9:
                            valor -= 9
                    suma += valor
                digito_control = str((10 - (suma % 10)) % 10)
                tarjeta += digito_control
                if suma % 10 == 0:
                    break

            # Generar la fecha de expiración y el CVV
            if len(mensaje) >= 3:
                # Usar la fecha especificada en el mensaje
                fecha = mensaje[2].split('|') if '|' in mensaje[2] else mensaje[2].split('/') 
                mes = fecha[0].zfill(2)
                ano = fecha[1]
            else:
                # Generar fecha aleatoria
                mes = str(random.randint(1, 12)).zfill(2)
                ano = str(random.randint(2024, 2030))
            cvv = ''.join(random.choice(string.digits) for _ in range(3))


            # Concatenar los valores y agregar a la lista
            tarjeta_completa = f"<code>{tarjeta}|{mes}|{ano}|{cvv}</code>"
            tarjetas_generadas.append(tarjeta_completa)

        # Enviar las tarjetas generadas
        bot.send_message(message.chat.id, '\n'.join(tarjetas_generadas), parse_mode='HTML')

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {e}")


bot.polling()
