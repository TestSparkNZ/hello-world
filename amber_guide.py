#!/usr/bin/env python3
"""
Interactive guide to help understand and test Amber Energy API
"""

import sys


def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def main():
    print_header("Amber Energy API - Understanding Guide")
    
    print("""
Amber Energy provides real-time wholesale electricity pricing for Australian
households. This guide will help you understand the API and what it means
for your inverter control strategy.
    """)
    
    print_header("Step 1: Getting Your API Token")
    print("""
1. Open your browser and go to: https://app.amber.com.au/
2. Log in with your Amber Energy credentials
3. Click on your profile (top right)
4. Go to 'Settings'
5. Find 'Developer Settings' or 'API Settings'
6. Enable 'Developer Mode'
7. Copy your API token (starts with 'psk_...')
8. Keep this token secure - treat it like a password!
    """)
    
    input("Press Enter when you have your API token...")
    
    print_header("Step 2: Understanding Amber Pricing")
    print("""
Amber shows you WHOLESALE electricity prices that change every 5-30 minutes.

KEY CONCEPTS:

1. PRICE DESCRIPTORS:
   - NEGATIVE: Grid is paying YOU to use electricity (rare but happens!)
   - LOW: Below average prices (good time to use power)
   - NEUTRAL: Average prices
   - HIGH: Above average prices
   - SPIKE: Very high prices (usually avoid)

2. CHANNEL TYPES:
   - GENERAL: Import price (what you pay to buy from grid)
   - FEED_IN: Export price (what you get paid for solar export)

3. PRICE in cents per kWh:
   - Negative (e.g., -5 c/kWh): You get PAID to use electricity
   - Low (e.g., 5 c/kWh): Cheap electricity
   - Normal (e.g., 15-25 c/kWh): Average
   - High (e.g., 35+ c/kWh): Expensive
   - Spike (e.g., 50+ c/kWh): Very expensive

4. RENEWABLES (%):
   - Shows percentage of renewable energy in the grid
   - Higher = more solar/wind in the grid
   - Often correlates with lower prices
    """)
    
    input("Press Enter to continue...")
    
    print_header("Step 3: Smart Battery Control Strategy")
    print("""
Using Amber prices, your system can make intelligent decisions:

CHARGE BATTERY when:
- Price is NEGATIVE (you get paid to charge!)
- Price is LOW and below your threshold (e.g., < 5 c/kWh)
- High renewable % and low prices (solar surplus)

DISCHARGE BATTERY when:
- Price is HIGH or SPIKE (save money, avoid expensive grid)
- Export price is HIGH (sell at good rates)
- Price is above your threshold (e.g., > 30 c/kWh)

NORMAL MODE when:
- Prices are NEUTRAL
- Standard solar self-consumption is optimal

EXAMPLE SCENARIO:

11 AM: Solar generating, price is LOW (10 c/kWh)
→ Normal mode, use solar for house, export surplus

2 PM: Price NEGATIVE (-5 c/kWh), lots of solar in grid
→ CHARGE battery from grid, get paid to store energy!

7 PM: Price SPIKE (45 c/kWh), everyone home, high demand
→ DISCHARGE battery, avoid expensive grid electricity

10 PM: Price normal (20 c/kWh)
→ Back to normal mode
    """)
    
    input("Press Enter to continue...")
    
    print_header("Step 4: Testing Your Setup")
    print("""
Before running the controller:

1. Test Amber API connection:
   $ python3 test_amber_api.py
   
   This will:
   - Connect to Amber API
   - Show your current prices
   - Display price forecast
   - Test decision logic

2. Test inverter controller:
   $ python3 test_inverter.py
   
   This will:
   - Test inverter communication (demo mode)
   - Show control commands
   - Verify framework is working

3. Run controller once (test mode):
   $ python3 smart_controller.py --once
   
   This will:
   - Get current prices
   - Make a decision
   - Show what action would be taken
   - NOT actually change inverter (until you implement control)

4. Run controller continuously:
   $ python3 smart_controller.py
   
   This will:
   - Monitor prices every 5 minutes
   - Automatically control inverter
   - Log all decisions
   - Run until you press Ctrl+C
    """)
    
    input("Press Enter to continue...")
    
    print_header("Step 5: Customizing Your Strategy")
    print("""
Edit config.yaml to customize your strategy:

CHARGE_THRESHOLD (default: 0.0 c/kWh):
- Set to 0: Only charge during negative pricing
- Set to 5: Charge when price is 5 c/kWh or less
- Set to 10: More aggressive charging

DISCHARGE_THRESHOLD (default: 30.0 c/kWh):
- Set to 25: Discharge earlier
- Set to 35: Only discharge during higher prices
- Consider your feed-in tariff rate

CHECK_INTERVAL (default: 300 seconds):
- 300s (5 min): Recommended for normal operation
- 600s (10 min): Less frequent checks
- 180s (3 min): More responsive (be careful of API limits!)

Remember: Amber API has rate limits (typically 100 calls/day)
At 5-minute intervals, that's 288 calls/day, so you might hit limits.
Consider 10-minute intervals (144 calls/day) for safety.
    """)
    
    input("Press Enter to continue...")
    
    print_header("Step 6: Important Safety Notes")
    print("""
⚠️  BEFORE RUNNING WITH REAL INVERTER CONTROL:

1. Battery Health:
   - Set min_battery_soc (don't discharge too low)
   - Set max_battery_soc (don't overcharge)
   - Respect manufacturer guidelines

2. Testing:
   - Run in test mode first (--once flag)
   - Monitor for at least 24 hours manually
   - Verify decisions make sense

3. Manual Override:
   - Keep manual control ability
   - Know how to stop the system
   - Have backup plan

4. Network Reliability:
   - Ensure stable internet
   - Have auto-normal-on-error enabled
   - Monitor system health

5. Compliance:
   - Check local grid regulations
   - Understand your electricity plan
   - Consider export limits

6. GoodWe Implementation:
   - Current code is a FRAMEWORK
   - You must implement actual inverter control
   - Test with inverter manufacturer support
    """)
    
    input("Press Enter to continue...")
    
    print_header("Step 7: Resources and Next Steps")
    print("""
RESOURCES:

1. Amber Energy:
   - Website: https://app.amber.com.au/
   - Developer Docs: https://app.amber.com.au/developers
   - Support: support@amber.com.au

2. GoodWe:
   - SEMS Portal: https://www.semsportal.com
   - Support: Contact GoodWe for API documentation
   - Community: Various solar forums and communities

3. This Project:
   - README.md: Full documentation
   - AMBER_GOODWE_INTEGRATION.md: Technical details
   - Source code: Well-commented for learning

NEXT STEPS:

1. Run: python3 test_amber_api.py (test API connection)
2. Edit: config.yaml (add your token and settings)
3. Run: python3 smart_controller.py --once (test decision logic)
4. Implement: GoodWe control for your specific model
5. Test: Thoroughly before deploying
6. Monitor: Watch the system for the first few days
7. Optimize: Adjust thresholds based on results

QUESTIONS?
- Check README.md for detailed documentation
- Open GitHub issue for bugs or questions
- Contact Amber/GoodWe support for API questions
    """)
    
    print_header("Setup Complete!")
    print("""
You now understand:
✓ How Amber Energy API works
✓ What the price data means
✓ How to make smart battery decisions
✓ How to test and configure the system
✓ Safety considerations

Good luck with your smart inverter controller!
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGuide interrupted. Run again anytime!")
        sys.exit(0)
