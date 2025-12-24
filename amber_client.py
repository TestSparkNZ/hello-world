"""
Amber Energy API Client

This module provides a simple interface to interact with Amber Energy's API
to retrieve electricity pricing information.

Documentation: https://app.amber.com.au/developers
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AmberClient:
    """Client for interacting with Amber Energy API"""
    
    BASE_URL = "https://api.amber.com.au/v1"
    
    def __init__(self, api_token: str):
        """
        Initialize Amber API client
        
        Args:
            api_token: Your Amber API token from developer settings
        """
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self.site_id = None
    
    def get_sites(self) -> List[Dict]:
        """
        Get list of sites associated with the account
        
        Returns:
            List of site information dictionaries
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/sites",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            sites = response.json()
            
            # Auto-select first site if available
            if sites and len(sites) > 0:
                self.site_id = sites[0].get('id')
                logger.info(f"Auto-selected site: {self.site_id}")
            
            return sites
        except requests.RequestException as e:
            logger.error(f"Error fetching sites: {e}")
            raise
    
    def get_current_prices(self, site_id: Optional[str] = None) -> Dict:
        """
        Get current electricity prices for a site
        
        Args:
            site_id: Site ID (uses auto-selected if not provided)
            
        Returns:
            Dictionary containing current price information with keys:
            - perKwh: Price in cents per kWh
            - descriptor: NEGATIVE, LOW, NEUTRAL, HIGH, or SPIKE
            - channelType: GENERAL (import) or FEED_IN (export)
            - renewables: Percentage of renewable energy
        """
        site_id = site_id or self.site_id
        if not site_id:
            raise ValueError("No site_id provided and no default site set")
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/sites/{site_id}/prices/current",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching current prices: {e}")
            raise
    
    def get_price_forecast(self, site_id: Optional[str] = None) -> List[Dict]:
        """
        Get price forecast for the next 24-48 hours
        
        Args:
            site_id: Site ID (uses auto-selected if not provided)
            
        Returns:
            List of price forecast dictionaries
        """
        site_id = site_id or self.site_id
        if not site_id:
            raise ValueError("No site_id provided and no default site set")
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/sites/{site_id}/prices",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching price forecast: {e}")
            raise
    
    def should_charge_battery(self, price_threshold: float = 0.0) -> bool:
        """
        Determine if battery should be charged based on current price
        
        Args:
            price_threshold: Price in cents per kWh below which to charge
            
        Returns:
            True if price is favorable for charging
        """
        try:
            prices = self.get_current_prices()
            
            # Find general usage price (import)
            for price_data in prices:
                if price_data.get('channelType') == 'GENERAL':
                    per_kwh = price_data.get('perKwh', float('inf'))
                    descriptor = price_data.get('descriptor', '')
                    
                    logger.info(f"Current price: {per_kwh:.2f} c/kWh ({descriptor})")
                    
                    # Charge if negative or below threshold
                    return per_kwh <= price_threshold or descriptor == 'NEGATIVE'
            
            return False
        except Exception as e:
            logger.error(f"Error determining charge decision: {e}")
            return False
    
    def should_discharge_battery(self, price_threshold: float = 30.0) -> bool:
        """
        Determine if battery should be discharged based on current price
        
        Args:
            price_threshold: Price in cents per kWh above which to discharge
            
        Returns:
            True if price is favorable for discharging
        """
        try:
            prices = self.get_current_prices()
            
            # Find feed-in price (export)
            for price_data in prices:
                if price_data.get('channelType') == 'FEED_IN':
                    per_kwh = price_data.get('perKwh', 0.0)
                    descriptor = price_data.get('descriptor', '')
                    
                    logger.info(f"Current feed-in price: {per_kwh:.2f} c/kWh ({descriptor})")
                    
                    # Discharge if high price or spike
                    return per_kwh >= price_threshold or descriptor in ['HIGH', 'SPIKE']
            
            return False
        except Exception as e:
            logger.error(f"Error determining discharge decision: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Replace with your actual API token
    API_TOKEN = "your_amber_api_token_here"
    
    client = AmberClient(API_TOKEN)
    
    # Get sites
    print("Fetching sites...")
    sites = client.get_sites()
    print(f"Found {len(sites)} site(s)")
    
    # Get current prices
    print("\nFetching current prices...")
    prices = client.get_current_prices()
    for price in prices:
        print(f"{price['channelType']}: {price['perKwh']:.2f} c/kWh ({price['descriptor']})")
    
    # Check battery decisions
    print(f"\nShould charge battery: {client.should_charge_battery()}")
    print(f"Should discharge battery: {client.should_discharge_battery()}")
