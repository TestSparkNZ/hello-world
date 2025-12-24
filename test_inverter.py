#!/usr/bin/env python3
"""
Example: Test GoodWe inverter controller (placeholder functionality)
"""

import sys
import logging
from goodwe_controller import GoodWeController, InverterMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print("\n" + "="*60)
    print("GoodWe Inverter Controller Test")
    print("="*60)
    
    print("\nNote: This is a template/framework.")
    print("Actual inverter control requires implementation based on")
    print("your specific inverter model and connection method.\n")
    
    # Get inverter serial number
    serial = input("Enter your inverter serial number (or press Enter for demo): ").strip()
    if not serial:
        serial = "DEMO_SERIAL_12345"
    
    try:
        # Initialize controller
        print(f"\n1. Initializing controller for inverter: {serial}")
        controller = GoodWeController(serial)
        
        # Get status
        print("\n2. Getting inverter status...")
        status = controller.get_status()
        print(f"   Status: {status['status']}")
        print(f"   Mode: {status['mode']}")
        print(f"   Power Output: {status['power_output']} W")
        print(f"   Battery SOC: {status['battery_soc']}%")
        
        # Test mode changes (in demo mode, these are placeholders)
        print("\n3. Testing mode changes...")
        
        print("\n   a) Setting to FORCE_CHARGE mode...")
        success = controller.force_charge(power_limit=3000)
        print(f"      Result: {'Success' if success else 'Failed'}")
        
        print("\n   b) Setting to NORMAL mode...")
        success = controller.set_normal_mode()
        print(f"      Result: {'Success' if success else 'Failed'}")
        
        print("\n   c) Setting to FORCE_DISCHARGE mode...")
        success = controller.force_discharge(power_limit=2000)
        print(f"      Result: {'Success' if success else 'Failed'}")
        
        print("\n   d) Returning to NORMAL mode...")
        success = controller.set_normal_mode()
        print(f"      Result: {'Success' if success else 'Failed'}")
        
        print("\n" + "="*60)
        print("✓ Test completed successfully!")
        print("\nIMPORTANT: To actually control your inverter, you need to:")
        print("1. Implement the _set_mode_sems() or _set_mode_modbus() method")
        print("2. Add proper authentication for SEMS API")
        print("3. Or configure Modbus TCP/IP with correct register addresses")
        print("4. Test thoroughly before connecting to real inverter!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logger.exception("Test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
