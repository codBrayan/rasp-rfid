from time import sleep

from gpiozero import RGBLED, Buzzer

from pi import config

led = RGBLED(
    config.PINO_LED_VERMELHO,
    config.PINO_LED_VERDE,
    config.PINO_LED_AZUL,
    active_high=not config.LED_ANODO_COMUM,
)

buzzer = Buzzer(config.PINO_BUZZER) if config.BUZZER_ATIVO else None

VERDE = (0, 1, 0)
AZUL = (0, 0, 1)
AMARELO = (1, 0.5, 0)
VERMELHO = (1, 0, 0)


def bipar(ligado, desligado, vezes):
    if buzzer:
        buzzer.beep(on_time=ligado, off_time=desligado, n=vezes)


def acender(cor, segundos):
    led.color = cor
    sleep(segundos)
    led.off()


def sinalizar(resultado):
    if resultado == "ENTRADA":
        bipar(0.1, 0.1, 1)
        acender(VERDE, 2)
    elif resultado == "SAIDA":
        bipar(0.1, 0.1, 2)
        acender(AZUL, 2)
    elif resultado == "NEGADO":
        bipar(0.8, 0.1, 1)
        acender(AMARELO, 2)
    elif resultado == "INVASAO":
        bipar(0.25, 0.25, 8)
        led.blink(on_time=0.25, off_time=0.25, on_color=VERMELHO, n=8, background=False)


if __name__ == "__main__":
    for resultado in ["ENTRADA", "SAIDA", "NEGADO", "INVASAO"]:
        print(resultado)
        sinalizar(resultado)
        sleep(1)
