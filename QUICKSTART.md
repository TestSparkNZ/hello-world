# Quick Start Guide

Get your Smart Inverter Controller up and running in 5 steps!

## Step 1: Get Your Amber API Token (5 minutes)

1. Visit: https://app.amber.com.au/
2. Log in to your account
3. Click your profile → Settings → Developer Settings
4. Enable "Developer Mode"
5. Copy your API token (starts with `psk_`)

**Keep this token secure!** Treat it like a password.

## Step 2: Install Dependencies (2 minutes)

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/TestSparkNZ/hello-world.git
cd hello-world

# Install Python packages
pip install -r requirements.txt
```

Or use the setup script:
```bash
bash setup.sh
```

## Step 3: Test Amber API Connection (3 minutes)

```bash
python3 test_amber_api.py
```

When prompted, enter your API token. You should see:
- Your site information
- Current electricity prices
- Price forecast
- Decision logic test results

If this works, you're successfully connected to Amber! 🎉

## Step 4: Understand How It Works (10 minutes)

Run the interactive guide:
```bash
python3 amber_guide.py
```

This will walk you through:
- How Amber pricing works
- What price descriptors mean
- How the smart controller makes decisions
- How to configure thresholds
- Safety considerations

## Step 5: Configure Your Settings (5 minutes)

Edit `config.yaml` with your information:

```yaml
amber:
  api_token: "your_actual_api_token"  # From Step 1

goodwe:
  serial_number: "your_inverter_serial"  # Find on inverter or SEMS portal

strategy:
  charge_threshold: 0.0      # Charge when price ≤ 0 c/kWh (negative)
  discharge_threshold: 30.0  # Discharge when price ≥ 30 c/kWh
  check_interval: 300        # Check every 5 minutes
```

## What's Next?

### For Testing (Recommended First!)

Run the controller once to see what it would do:
```bash
python3 smart_controller.py --once
```

This will:
- Get current prices
- Make a decision
- Show what action would be taken
- NOT actually control the inverter yet

### For Production Use

**IMPORTANT**: Before running in production:

1. **Implement GoodWe Control**: The current code is a framework. You need to:
   - Complete the SEMS API integration, OR
   - Implement Modbus TCP/IP control
   - Test with your specific inverter model

2. **Test Thoroughly**: 
   - Run in test mode for several days
   - Verify decisions make sense
   - Monitor manually

3. **Set Safety Limits**:
   - Configure `min_battery_soc` (e.g., 20%)
   - Configure `max_battery_soc` (e.g., 95%)
   - Enable `auto_normal_on_error`

4. **Run Continuously**:
```bash
python3 smart_controller.py
```

Press Ctrl+C to stop (it will return inverter to normal mode).

## Typical Price Scenarios

### Scenario 1: Sunny Day, High Solar Generation
- **Time**: 11 AM - 2 PM
- **Price**: -5 to 5 c/kWh (NEGATIVE or LOW)
- **Action**: CHARGE battery from grid (you get paid!)
- **Why**: Excess solar in grid, prices go negative

### Scenario 2: Evening Peak
- **Time**: 6 PM - 9 PM
- **Price**: 35-50 c/kWh (HIGH or SPIKE)
- **Action**: DISCHARGE battery to reduce grid usage
- **Why**: High demand, expensive electricity

### Scenario 3: Overnight
- **Time**: 12 AM - 6 AM
- **Price**: 15-20 c/kWh (NEUTRAL)
- **Action**: NORMAL mode
- **Why**: Standard pricing, use battery as needed

## Troubleshooting

### "Failed to connect to Amber API"
- Check your API token is correct (copy-paste carefully)
- Verify internet connection
- Ensure Developer Mode is enabled in Amber settings

### "No sites found"
- Your API token might be for a different account
- Check you're logged into the correct Amber account
- Contact Amber support if issue persists

### "Inverter not responding"
- The framework needs implementation for your specific inverter
- Check `goodwe_controller.py` comments for implementation details
- Verify inverter network connectivity
- Contact GoodWe for API documentation

## Running as a Background Service

Once tested and working, run as a service:

### On Linux (systemd):
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

Enable:
```bash
sudo systemctl enable smart-inverter
sudo systemctl start smart-inverter
```

Check status:
```bash
sudo systemctl status smart-inverter
```

View logs:
```bash
sudo journalctl -u smart-inverter -f
```

## Need Help?

- **Understanding Amber API**: Run `python3 amber_guide.py`
- **Full Documentation**: Read `README.md`
- **Technical Details**: Read `AMBER_GOODWE_INTEGRATION.md`
- **Amber Support**: https://help.amber.com.au/
- **GoodWe Support**: Contact GoodWe for API docs

## Safety Checklist

Before running in production:

- [ ] Tested with `--once` flag multiple times
- [ ] Verified decisions align with prices
- [ ] Set battery SOC limits (min/max)
- [ ] Have manual override capability
- [ ] Monitored for 24-48 hours manually
- [ ] Verified compliance with grid regulations
- [ ] Tested error handling (disconnect internet, etc.)
- [ ] Set up logging and monitoring
- [ ] Informed household members about automation
- [ ] Have emergency shutdown procedure

## Support & Community

- GitHub Issues: Report bugs or ask questions
- Amber Community: https://www.ambercommunity.com.au/
- Solar Forums: Share experiences and get advice

---

**Ready to save money with smart battery control!** ⚡🔋☀️

Remember: Start with testing, verify everything works, then deploy carefully.
