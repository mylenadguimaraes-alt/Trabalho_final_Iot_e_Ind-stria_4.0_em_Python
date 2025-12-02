import threading
import time

try:
    import serial
    ARDUINO_AVAILABLE = True
except:
    ARDUINO_AVAILABLE = False

class ArduinoController:
    def __init__(self, porta="/dev/ttyACM0"):
        self.callback = None
        self.simulation = False

        if not ARDUINO_AVAILABLE:
            print("PySerial não encontrado. Entrando em modo simulação.")
            self.simulation = True
            return

        try:
            self.ser = serial.Serial(porta, 9600, timeout=1)
            self.thread = threading.Thread(target=self.listen, daemon=True)
            self.thread.start()
        except Exception as e:
            print(f"Não foi possível conectar ao Arduino: {e}")
            print("Entrando em modo simulação.")
            self.simulation = True

    def listen(self):
        while True:
            try:
                msg = self.ser.readline().decode().strip()
                if msg and self.callback:
                    self.callback(msg)
            except Exception:
                pass

    # ---------------- COMANDOS ----------------
    def arm_system(self):
        if self.simulation:
            print("[SIM] arm_system")
            if self.callback:
                self.callback("Sistema_armado")
        else:
            self.ser.write(b'arm_system\n')

    def disarm_system(self):
        if self.simulation:
            print("[SIM] disarm_system")
            if self.callback:
                self.callback("Sistema_desarmado")
        else:
            self.ser.write(b'disarm_system\n')

    def stop_alarm(self):
        if self.simulation:
            print("[SIM] stop_alarm")
            if self.callback:
                self.callback("Alarme_parado")
        else:
            self.ser.write(b'stop_alarm\n')

    def authorize(self):
        if self.simulation:
            print("[SIM] authorize")
            if self.callback:
                self.callback("Autorizacao_recebida")
        else:
            self.ser.write(b'authorize\n')
    # Adicione este método na classe ArduinoController:

    def enable_auto_rearm(self):
        if self.simulation:
            print("[SIM] enable_auto_rearm")
            if self.callback:
                self.callback("Auto_rearm_enabled")
        else:
            self.ser.write(b'enable_auto_rearm\n')
