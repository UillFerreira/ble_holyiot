import asyncio
import signal
import requests
from bleak import BleakScanner
from typing import Optional

# MAC address alvo (filtrar apenas esse)
TARGET_MAC = "EA:7F:D4:C4:BC:71"
# UUID do ServiceData do beacon
TARGET_UUID = "00005242-0000-1000-8000-00805f9b34fb"
# Última temperatura válida
last_valid_temperature = None

def parse_beacon(data: bytes) -> dict:
    if len(data) < 23 or data[0] != 0x02 or data[1] != 0x15:
        raise ValueError("Formato inválido de pacote iBeacon")
    uuid = data[2:18]
    return {
        "uuid": f"{uuid.hex()[0:8]}-{uuid.hex()[8:12]}-{uuid.hex()[12:16]}-{uuid.hex()[16:20]}-{uuid.hex()[20:]}",
        "major": int.from_bytes(data[18:20], "big"),
        "minor": int.from_bytes(data[20:22], "big"),
        "tx_power": int.from_bytes(data[22:23], "big", signed=True),
    }

def parse_sensor_data(data: bytes):
    if len(data) < 12:
        raise ValueError("Dados devem ter ao menos 12 bytes")

    # Os últimos 3 bytes são os que importam para leitura do sensor
    sensor_type = data[-3]
    raw_value = int.from_bytes(data[-2:], byteorder='big')  # últimos 2 bytes como inteiro

    if sensor_type == 0x01:
        temperatura = raw_value / 250.0
        return {"sensor": "temperatura", "valor": temperatura}

    elif sensor_type == 0x03:
        umidade = raw_value / 256.0
        return {"sensor": "umidade", "valor": umidade}

    elif sensor_type == 0x04:
        vibrando = raw_value == 0x0100
        return {"sensor": "vibracao", "valor": vibrando}

    elif sensor_type == 0x06:
        botao_pressionado = raw_value == 0x0100
        return {"sensor": "botao", "valor": botao_pressionado}

    else:
        return {"sensor": f"desconhecido (0x{sensor_type:02x})", "valor": raw_value}

def handle_advertisement(device, advertisement_data):

    if device.address.upper() != TARGET_MAC:
        return  # Ignorar dispositivos que não são o alvo
    #print(f"Raw data: {advertisement_data}")
#   print(f"\n📡 Dispositivo detectado: {device.address}")
#   print(f"Nome: {device.name}")
    #print(f"RSSI: {device.rssi} dBm")
    # Dados do fabricante (iBeacon)
    if advertisement_data.manufacturer_data:
        for key, value in advertisement_data.manufacturer_data.items():
            #print(f"data: {value.hex()}")
            pvalue = parse_beacon(value)
            #print(f"tx-power: {pvalue['tx_power']}")
    #print(f"UUID: {advertisement_data.service_uuids}")
    # ServiceData
    for uuid, value_sdata in advertisement_data.service_data.items():
#       print(f"  🧪 ServiceData UUID: {uuid}")
        sensor = parse_sensor_data(value_sdata)
        print(f"data: {value_sdata.hex()}");
        print(f"Valores: {sensor}");

async def main():
    scanner = BleakScanner()
    scanner.register_detection_callback(handle_advertisement)
    print("🔍 Escaneando apenas o dispositivo BLE com MAC EA:7F:D4:C4:BC:71 (Ctrl+C para sair)...")
    await scanner.start()
    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrando scanner BLE.")
        await scanner.stop()

if __name__ == "__main__":
    asyncio.run(main())
        
