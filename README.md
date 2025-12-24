# Smart Inverter Controller

An intelligent application that integrates **Amber Energy** dynamic pricing with **GoodWe inverter** control to optimize solar energy usage and reduce electricity costs.

## Overview

This application monitors real-time electricity prices from Amber Energy and automatically controls your GoodWe inverter to:
- **Charge battery** during low/negative price periods
- **Discharge battery** during high price periods
- **Maximize savings** by optimizing grid interaction based on live pricing

## Features

- ✅ Real-time electricity price monitoring via Amber Energy API
- ✅ Intelligent battery charge/discharge decisions
- ✅ GoodWe inverter control framework (SEMS API & Modbus support)
- ✅ Configurable price thresholds
- ✅ Safety controls and limits
- ✅ Comprehensive logging and monitoring
- ✅ Easy to customize and extend

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Amber Energy account with API access
- GoodWe inverter with network connectivity
- Basic understanding of Python

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/TestSparkNZ/hello-world.git
cd hello-world

# Install dependencies
pip install -r requirements.txt
```

### 3. Get Your Amber API Token

1. Log in to [Amber Energy](https://app.amber.com.au/)
2. Go to **Settings** → **Developer Settings**
3. Enable **Developer Mode**
4. Copy your **API Token**

### 4. Configure the Application

Edit `config.yaml` with your details:

```yaml
amber:
  api_token: "your_amber_api_token_here"

goodwe:
  serial_number: "your_inverter_serial_here"
  connection_type: "sems"  # or "modbus"

strategy:
  charge_threshold: 0.0      # Charge when price ≤ 0 c/kWh
  discharge_threshold: 30.0  # Discharge when price ≥ 30 c/kWh
  check_interval: 300        # Check every 5 minutes
```

### 5. Test Your Setup

Test Amber API connection:
```bash
python test_amber_api.py
```

Test inverter controller (demo mode):
```bash
python test_inverter.py
```

### 6. Run the Controller

Run once (test mode):
```bash
python smart_controller.py --once
```

Run continuously:
```bash
python smart_controller.py
```

## Understanding Amber Energy API

Amber provides real-time wholesale electricity pricing. The API returns:

- **perKwh**: Current price in cents per kWh
- **descriptor**: Price status (NEGATIVE, LOW, NEUTRAL, HIGH, SPIKE)
- **channelType**: GENERAL (import) or FEED_IN (export)
- **renewables**: Percentage of renewable energy in the grid

### Example API Response

```json
[
  {
    "channelType": "GENERAL",
    "perKwh": -5.2,
    "descriptor": "NEGATIVE",
    "renewables": 78.5
  },
  {
    "channelType": "FEED_IN",
    "perKwh": 8.5,
    "descriptor": "LOW"
  }
]
```

## GoodWe Inverter Control

The application provides a framework for controlling GoodWe inverters through two methods:

### Option 1: SEMS Cloud API
- Remote control via internet
- Requires SEMS account credentials
- Implementation requires API documentation (contact GoodWe)

### Option 2: Modbus TCP/IP
- Local network control
- Faster and more reliable
- Requires inverter IP and Modbus register map
- Install additional library: `pip install pymodbus`

**Note**: The current implementation provides a framework. You'll need to complete the integration based on your specific inverter model and available documentation.

## How It Works

### Control Logic

1. **Every 5 minutes** (configurable):
   - Fetch current electricity prices from Amber
   - Analyze import and export prices
   - Make a decision based on configured thresholds

2. **Decision Matrix**:
   - **CHARGE**: Import price ≤ threshold OR negative pricing
   - **DISCHARGE**: Export price ≥ threshold OR high import price
   - **NORMAL**: Standard solar operation

3. **Apply Control**:
   - Send commands to GoodWe inverter
   - Log decision and outcome
   - Wait for next check interval

### Example Scenarios

**Scenario 1: Negative Pricing**
- Import: -5 c/kWh (NEGATIVE)
- Decision: **CHARGE** battery from grid
- Result: Get paid to charge your battery!

**Scenario 2: Price Spike**
- Import: 45 c/kWh (SPIKE)
- Export: 35 c/kWh (HIGH)
- Decision: **DISCHARGE** battery to grid
- Result: Reduce grid usage and sell at high rates

**Scenario 3: Normal Operation**
- Import: 15 c/kWh (NEUTRAL)
- Export: 8 c/kWh (LOW)
- Decision: **NORMAL** mode
- Result: Standard solar self-consumption

## Configuration Options

### Price Thresholds

Adjust these based on your electricity plan:

```yaml
strategy:
  # When to charge (cents per kWh)
  charge_threshold: 0.0
  
  # When to discharge (cents per kWh)
  discharge_threshold: 30.0
```

### Safety Limits

Protect your battery:

```yaml
safety:
  min_battery_soc: 20   # Don't discharge below 20%
  max_battery_soc: 95   # Don't charge above 95%
```

### Check Interval

How often to check prices:

```yaml
strategy:
  check_interval: 300   # 5 minutes (recommended)
```

⚠️ **Don't check too frequently** - Amber API has rate limits, and inverter mode changes should not be too frequent.

## Project Structure

```
├── README.md                          # This file
├── AMBER_GOODWE_INTEGRATION.md       # Detailed integration guide
├── config.yaml                        # Configuration file
├── requirements.txt                   # Python dependencies
├── amber_client.py                    # Amber Energy API client
├── goodwe_controller.py               # GoodWe inverter controller
├── smart_controller.py                # Main application
├── test_amber_api.py                  # Test Amber API connection
└── test_inverter.py                   # Test inverter controller
```

## Safety and Best Practices

⚠️ **Important Safety Considerations**:

1. **Test Thoroughly**: Run in demo mode first
2. **Monitor Initially**: Watch the first few cycles closely
3. **Battery Limits**: Configure safe SOC limits
4. **Manual Override**: Always have a way to manually control your inverter
5. **Network Reliability**: Ensure stable internet for API calls
6. **Error Handling**: The app returns to normal mode on errors
7. **Grid Compliance**: Ensure compliance with local grid regulations

## Troubleshooting

### "Failed to connect to Amber API"
- Check your API token is correct
- Verify your Amber account has API access enabled
- Check internet connectivity

### "Inverter control not working"
- The current implementation is a framework
- Implement `_set_mode_sems()` or `_set_mode_modbus()` based on your setup
- Check inverter network connectivity
- Verify inverter serial number

### "Rate limit errors"
- Increase `check_interval` to reduce API calls
- Amber API has rate limits (typically 100 calls/day)

## Advanced Usage

### Running as a Service (Linux)

Create a systemd service to run continuously:

```bash
sudo nano /etc/systemd/system/smart-inverter.service
```

Add:
```ini
[Unit]
Description=Smart Inverter Controller
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/hello-world
ExecStart=/usr/bin/python3 smart_controller.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable smart-inverter
sudo systemctl start smart-inverter
sudo systemctl status smart-inverter
```

## Further Reading

- [Amber Energy Developer Docs](https://app.amber.com.au/developers)
- [GoodWe SEMS Portal](https://www.semsportal.com)
- [Integration Guide](AMBER_GOODWE_INTEGRATION.md)

## Contributing

This is a template/framework project. Contributions welcome:
- Complete SEMS API integration
- Add Modbus implementation
- Improve decision algorithms
- Add web dashboard
- Support for other inverter brands

## License

This project is provided as-is for educational and personal use.

## Disclaimer

⚠️ **Use at your own risk**. This software controls electrical equipment. The authors are not responsible for any damage, financial loss, or safety issues resulting from the use of this software. Always ensure proper safety measures and compliance with local regulations.

---

## Support

For questions about:
- **Amber API**: Contact Amber Energy support
- **GoodWe Inverters**: Contact GoodWe support
- **This Project**: Open an issue on GitHub

Happy optimizing! ⚡🔋☀️
