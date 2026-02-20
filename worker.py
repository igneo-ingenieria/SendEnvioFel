import time
import logging

from c_factorial import Factorial

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():

    if Factorial().proceso_cumpleaños():
        time.sleep(86400) # 24 horas hasta la proxima ejecucion si no da error
        main()
    else:
        time.sleep(900) # 15 minutos hasta la proxima ejecucion, si da error
        main()

if __name__ == "__main__":
    main()
