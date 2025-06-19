# BLE Beacon Decoder - HolyIot Python Scanner

Projeto em Python para escanear, filtrar e decodificar pacotes BLE (Bluetooth Low Energy) de um beacon da marca **HolyIot**, utilizando a biblioteca [Bleak](https://github.com/hbldh/bleak).

---

## 🎯 Objetivo

Capturar anúncios (advertisements) BLE próximos, filtrar por um beacon específico e decodificar os dados enviados (ex.: temperatura, umidade, sensores de movimento, etc).

---

## ✅ Estado Atual

- ✔️ Captura de pacotes BLE usando o **BleakScanner**
- ✔️ Filtro por **endereço MAC fixo** (por enquanto manual no código)
- ✔️ Decodificação parcial dos dados do beacon (sensores principais já mapeados)
- ✔️ Estrutura de código pronta para expandir com novos sensores e formatos de payload

---

## 🚧 Próximos Passos (Roadmap)

- [ ] Parametrização via input/config para escolher o MAC de interesse
- [ ] Captura do nível de bateria
- [ ] Implementação de envio de comandos para o beacon (para alteração de configurações do dispositivo)
- [ ] Possibilidade de enviar os dados para uma API externa (URL configurável)

---

## 🧱 Dependências

- Python 3.8+
- Bleak (>= 0.20.0)

Instalação das dependências:

```bash
pip install bleak
```

## ▶️ Como Rodar
Por enquanto, o MAC address do beacon está fixo dentro do código.

Exemplo básico de execução:
```
python ble_decoder.py
```
# Decodificação de Pacotes iBeacon

Este projeto lida com pacotes BLE no formato iBeacon. Abaixo está a documentação da estrutura dos dados recebidos e como interpretá-los.

---

## 📦 Exemplo de pacote (em hexadecimal)

```
0215fda50693a4e24fb1afcfc6eb07647825271b4cb9c9
```

---

## 🧩 Estrutura do pacote iBeacon

| Campo           | Posição (hex) | Tamanho (bytes) | Descrição                                                               |
| --------------- | ------------- | --------------- | ----------------------------------------------------------------------- |
| Prefixo iBeacon | `0x00 - 0x01` | 2               | **`0x02 0x15`** - Identifica pacote iBeacon e tamanho, no caso 21 bytes |
| UUID            | `0x02 - 0x11` | 16              | Identificador único do beacon                                           |
| Major           | `0x12 - 0x13` | 2               | Identificador para agrupamento de beacons                               |
| Minor           | `0x14 - 0x15` | 2               | Identificador secundário dentro do grupo                                |
| Tx Power        | `0x16`        | 1               | Potência de transmissão (RSSI a 1 metro)                                |

---

# Formato dos Dados dos Sensores (Beacon Holyiot 22049 - NRF52810)

Cada pacote de sensor contém 12 bytes.

| Bytes  | Descrição                    | Observações                                                                                                                      |
| ------ | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 0 a 7  | Endereço/ID do Beacon        | 8 bytes fixos por dispositivo (exemplo: `415fea7fd4c4bc71`)                                                                      |
| 8      | Tipo de Sensor (Sensor Type) | Indica qual sensor gerou o valor:<br> - `0x01` = Temperatura<br> - `0x03` = Umidade<br> - `0x04` = Vibração<br> - `0x06` = Botão |
| 9 a 10 | Valor do Sensor (Big Endian) | Interpretação depende do tipo de sensor (ver tabela abaixo)                                                                      |
| 11     | Reservado / Não usado        | Em geral, está vindo como `0x00`, pode ser reservado para uso futuro                                                             |

## Interpretação do campo "Valor" (Bytes 9 e 10)

Ex: `415fea7fd4c4bc71040601152e`

| Tipo de Sensor       | Descrição                                                                       | Exemplo de Valor Hex | Resultado Exemplo |
| -------------------- | ------------------------------------------------------------------------------- | -------------------- | ----------------- |
| `0x01` - Temperatura | Inteiro sem sinal. Fórmula: **valor / 250**<br>Unidade: °C                      | `0x152E`             | **21,68°C**       |
| `0x03` - Umidade     | Inteiro sem sinal. Fórmula: **valor / 256**<br>Unidade: %                       | `0x3A15`             | **58,08%**        |
| `0x04` - Vibração    | Estado binário:<br>- `0x0100` = Vibração detectada<br>- `0x0000` = Sem vibração | `0x0100` ou `0x0000` | True / False      |
| `0x06` - Botão       | Estado binário:<br>- `0x0100` = Pressionado<br>- `0x0000` = Não pressionado     | `0x0100` ou `0x0000` | True / False      |

## 📌 Observações
Este projeto está em desenvolvimento e aberto para evoluções futuras.

## Contribuições
Pull requests, issues e sugestões são bem-vindas!
Se tiver algum beacon HolyIot similar e quiser ajudar com a decodificação de outros modelos/sensores, sinta-se à vontade para colaborar.

## 📃 Licença
Este projeto está licenciado sob os termos da [Licença MIT](LICENSE).

---
## 📌 Sobre o autor

**William Costa Ferreira**  
💼 Desenvolvedor Full Stack  
🌎 Brasil

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/william-costa-ferreira)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/william-costa-ferreira-9238b927/)
