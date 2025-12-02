int analogPin = A0;   // AO do TCRT5000
int buzzerPin = 3;    // pino digital do buzzer
int limite = 400;

unsigned long authorize_time = 0;
const long authorize_timeout = 30000;  // 30s autorizado
bool was_closed = true;

bool alarm_triggered = false;
bool alarm_muted = false;  // true = alarme silenciado, false = alarme pode tocar

bool system_armed = true;

void setup() {
  Serial.begin(9600);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
  int valor = analogRead(analogPin);
  bool is_open = (valor > limite);

  // --- COMANDOS SERIAL ---
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "authorize") {
      authorize_time = millis();
      alarm_triggered = false;
      Serial.println("Autorizacao_recebida");

    } else if (cmd == "stop_alarm") {
      // Desativa completamente o alarme
      alarm_triggered = false;
      alarm_muted = true;  // Mantém o alarme silenciado
      digitalWrite(buzzerPin, LOW);
      Serial.println("Alarme_parado");

    } else if (cmd == "arm_system") {
      system_armed = true;
      // Não altera o estado do alarme existente
      digitalWrite(buzzerPin, HIGH);
      delay(200);
      digitalWrite(buzzerPin, LOW);
      Serial.println("Sistema_armado");

    } else if (cmd == "disarm_system") {
      // Desarma o sistema e para o alarme
      system_armed = false;
      alarm_triggered = false;
      alarm_muted = true;  // Mantém o alarme silenciado
      digitalWrite(buzzerPin, LOW);
      Serial.println("Sistema_desarmado");
    }
  }

  bool authorized = (authorize_time > 0) && (millis() - authorize_time < authorize_timeout);

  // --- DETECTA ABERTURA DA PORTA ---
  if (is_open && was_closed) {
    if (authorized) {
      Serial.println("authorized_open");
    } else if (system_armed) {
      Serial.println("unauthorized_open");
      alarm_triggered = true;
      alarm_muted = false;  // Permite que o alarme toque
    } else {
      Serial.println("open_but_system_off");
    }
  }

  // --- LÓGICA DO ALARME ---
  // O alarme toca apenas se estiver disparado E não estiver silenciado
  if (alarm_triggered && !alarm_muted) {
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(buzzerPin, LOW);
  }

  was_closed = !is_open;
  delay(150);
}
