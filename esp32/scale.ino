#include <Arduino.h>
#include "BLEDevice.h"
#include "BLEUtils.h"
#include "BLEBeacon.h"
#include "BLEAdvertising.h"
#include "BLEEddystoneURL.h"
#include <Wire.h>
#include "SSD1306.h"//ディスプレイ用ライブラリを読み込み
#include "HX711.h"
#include "esp_sleep.h"

const int DT_PIN = 27;
const int SCK_PIN = 33;
const int QUEUE_LEN = 5;
const float THRESHOLD = 0.2;

float queue[QUEUE_LEN];
bool flgM = true;

HX711 scale;
SSD1306 display(0x3c, 21, 22); //SSD1306インスタンスの作成（I2Cアドレス,SDA,SCL）
BLEAdvertising *pAdvertising;

#define BEACON_UUID "8ec76ea3-6668-48da-9866-75be8bc86f4d" // UUID 1 128-Bit (may use linux tool uuidgen or random numbers via https://www.uuidgenerator.net/)

void setBeacon(float weight)
{
  uint16_t beconUUID = 0xFEAB;

  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();
  BLEAdvertisementData oScanResponseData = BLEAdvertisementData();

  oScanResponseData.setFlags(0x06); // GENERAL_DISC_MODE 0x02 | BR_EDR_NOT_SUPPORTED 0x04
  oScanResponseData.setCompleteServices(BLEUUID(beconUUID));

  char buff[30];
  sprintf(buff ,"%7.1f" ,weight);
  std::string str = std::string(buff);

  oScanResponseData.setServiceData(BLEUUID(beconUUID), str);
  oAdvertisementData.setName("ScaleBeacon");
  pAdvertising->setAdvertisementData(oAdvertisementData);
  pAdvertising->setScanResponseData(oScanResponseData);
}

void initBLEBeacon(){
  BLEDevice::init("ScaleBeacon");
  BLEDevice::setPower(ESP_PWR_LVL_N12);
  pAdvertising = BLEDevice::getAdvertising();
}

void setup() {

  Serial.begin(115200);
  scale.begin(DT_PIN, SCK_PIN);

  // パラメータ設定
  scale.set_scale(483.3);
  scale.tare();

  // キューを初期化
  initQueue();

  // ディスプレイを初期化
  display.init();    

  // BLEを初期化
  initBLEBeacon();
}

// キュー初期化
void initQueue(){

  for (int i=0 ; i<QUEUE_LEN ; i++){
    queue[i] = 0;
  }
  queue[QUEUE_LEN] = '\n';

}

// キューに登録
void appendQueue(float weight) {

  for (int i=0 ; i<QUEUE_LEN-1 ; i++){
    queue[i] = queue[i+1];
  }
  queue[QUEUE_LEN-1] = weight;

}

// キューを評価 
bool evalQueue(void) {

  float tmpW = queue[0];
  for (int i=1 ; i<QUEUE_LEN ; i++){
    if ((tmpW - THRESHOLD) >= queue[i]){
      return false;
    }
    if ((tmpW + THRESHOLD) <= queue[i]){
      return false;
    }
  }

  // すべて同じなら値を返却
  return true;
}

void loop() {

  float weight;
  char strWeight[7];

  //重量を取得（小数点１位は四捨五入）
  weight = float(scale.get_units(3) + 0.05);
  if (weight < 0.2) weight = 0.0;

  //重量表示
  sprintf(strWeight ,"%7.1f g" ,weight);

  // キューに追加
  appendQueue(weight);

  // ディスプレイを更新
  display.clear();
  display.setFont(ArialMT_Plain_24);    
  display.drawString(32, 16, strWeight);

  if (evalQueue()){
    // 重量が安定
    display.drawLine(24, 44, 104 ,44);
    setBeacon(weight);  //データをビーコンにセット
    flgM = true;
  } else {
    // 重量が不安定
    display.setFont(ArialMT_Plain_16);    
    flgM = !flgM;
  }
  display.display();

  // Beaconからアドバタイズパケット送信
  pAdvertising->start();
  Serial.printf("Advertizing started (weight:%7.1f g)...\n",weight);
  delay(50);

}