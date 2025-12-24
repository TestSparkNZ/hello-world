#!/usr/bin/env python3
"""
Example: Test Amber Energy API connection and view current prices
"""

import sys
import logging
from amber_client import AmberClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Replace with your actual API token
    api_token = input("Enter your Amber API token: ").strip()
    
    if not api_token:
        print("Error: No API token provided")
        sys.exit(1)
    
    try:
        print("\n" + "="*60)
        print("Amber Energy API Test")
        print("="*60)
        
        # Initialize client
        client = AmberClient(api_token)
        
        # Get sites
        print("\n1. Fetching your sites...")
        sites = client.get_sites()
        print(f"   Found {len(sites)} site(s)")
        for site in sites:
            print(f"   - Site ID: {site.get('id')}")
            print(f"     Address: {site.get('address', 'N/A')}")
        
        if not sites:
            print("   No sites found. Check your API token.")
            sys.exit(1)
        
        # Get current prices
        print("\n2. Fetching current electricity prices...")
        prices = client.get_current_prices()
        
        print("\n   Current Prices:")
        for price_data in prices:
            channel = price_data.get('channelType')
            per_kwh = price_data.get('perKwh')
            descriptor = price_data.get('descriptor')
            renewables = price_data.get('renewables', 0)
            
            print(f"\n   {channel}:")
            print(f"   - Price: {per_kwh:.2f} c/kWh")
            print(f"   - Status: {descriptor}")
            if channel == 'GENERAL':
                print(f"   - Renewables: {renewables:.1f}%")
        
        # Get price forecast
        print("\n3. Fetching price forecast...")
        forecast = client.get_price_forecast()
        
        if forecast:
            print(f"   Retrieved {len(forecast)} forecast periods")
            print("\n   Next few periods:")
            
            # Show first 6 forecast periods
            for i, period in enumerate(forecast[:6]):
                if period.get('channelType') == 'GENERAL':
                    start_time = period.get('startTime', 'N/A')
                    per_kwh = period.get('perKwh')
                    descriptor = period.get('descriptor')
                    print(f"   {start_time}: {per_kwh:.2f} c/kWh ({descriptor})")
        
        # Test decision logic
        print("\n4. Testing decision logic...")
        should_charge = client.should_charge_battery(price_threshold=5.0)
        should_discharge = client.should_discharge_battery(price_threshold=30.0)
        
        print(f"   Should charge battery: {should_charge}")
        print(f"   Should discharge battery: {should_discharge}")
        
        print("\n" + "="*60)
        print("✓ Test completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logger.exception("Test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
