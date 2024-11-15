#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup()
{
  Serial.begin(9600);
  while (!Serial); // Para o Leonardo/Micro
  Serial.println("Iniciando o sensor de digitais JM-101B 2020T...");

  finger.begin(57600);
  if (finger.verifyPassword()) {
    Serial.println("Sensor de digitais detectado!");
  } else {
    Serial.println("Não foi possível encontrar o sensor.");
    while (1); // Para o código caso o sensor não seja encontrado
  }
}

void loop()
{
  Serial.println("Pressione o dedo para captura do ID.");
  if (finger.getImage() == FINGERPRINT_OK) {
    Serial.println("Digital capturada, registrando...");
    int userID = registerFingerprint();

    if (userID > 0) {
      // Envia o fingerID para o Python
      Serial.print("fingerID: ");
      Serial.println(userID);
    }
  } else {
    Serial.println("Nenhum dedo detectado.");
  }

  delay(2000);
}

int registerFingerprint() {
  int id = findNextAvailableID();
  if (id == -1) {
    Serial.println("Sem espaço para novos cadastros.");
    return -1;
  }

  Serial.println("Posicione o dedo no sensor novamente para confirmar.");
  delay(2000);
  if (finger.image2Tz() != FINGERPRINT_OK) {
    Serial.println("Erro ao converter imagem.");
    return -1;
  }

  Serial.println("Armazenando digital...");
  if (finger.createModel() == 10) {
    if (finger.storeModel(id) == FINGERPRINT_OK) {
      Serial.print("Digital registrada com ID: ");
      Serial.println(id);
      return id;
    } else {
      Serial.println("Erro ao armazenar digital.");
      Serial.println(id);
    }
  } else {
    Serial.println("Erro ao criar modelo.");
    Serial.println(finger.createModel());

  }
  return -1;
}

// Função para encontrar o próximo ID disponível
int findNextAvailableID() {
  for (int i = 1; i < 256; i++) {
    if (!finger.loadModel(i)) { // Verifica se há um slot livre no sensor
      return i;
    }
  }
  return -1; // Nenhum ID disponível
}