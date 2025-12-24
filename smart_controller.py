"""
Smart Inverter Controller

Integrates Amber Energy pricing with GoodWe inverter control
to optimize battery usage and reduce electricity costs.

This application:
1. Monitors electricity prices from Amber Energy
2. Makes intelligent decisions about battery charging/discharging
3. Controls GoodWe inverter based on price signals
"""

import logging
import time
from typing import Optional
import json
from datetime import datetime

from amber_client import AmberClient
from goodwe_controller import GoodWeController, InverterMode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SmartInverterController:
    """
    Main controller that integrates Amber pricing with GoodWe inverter
    """
    
    def __init__(
        self,
        amber_api_token: str,
        inverter_sn: str,
        charge_threshold: float = 0.0,  # Charge when price <= 0 c/kWh
        discharge_threshold: float = 30.0,  # Discharge when price >= 30 c/kWh
        check_interval: int = 300  # Check every 5 minutes
    ):
        """
        Initialize the smart controller
        
        Args:
            amber_api_token: Amber Energy API token
            inverter_sn: GoodWe inverter serial number
            charge_threshold: Price threshold for charging (c/kWh)
            discharge_threshold: Price threshold for discharging (c/kWh)
            check_interval: How often to check prices (seconds)
        """
        self.amber = AmberClient(amber_api_token)
        self.inverter = GoodWeController(inverter_sn)
        self.charge_threshold = charge_threshold
        self.discharge_threshold = discharge_threshold
        self.check_interval = check_interval
        
        # Initialize Amber client
        try:
            self.amber.get_sites()
            logger.info("Successfully connected to Amber Energy API")
        except Exception as e:
            logger.error(f"Failed to connect to Amber API: {e}")
            raise
        
        self.current_strategy = "normal"
        logger.info("Smart Inverter Controller initialized")
    
    def get_current_price_info(self) -> dict:
        """
        Get current price information from Amber
        
        Returns:
            Dictionary with import and export prices
        """
        try:
            prices = self.amber.get_current_prices()
            
            price_info = {
                "timestamp": datetime.now().isoformat(),
                "import_price": None,
                "export_price": None,
                "import_descriptor": None,
                "export_descriptor": None,
                "renewables": None
            }
            
            for price_data in prices:
                channel = price_data.get('channelType')
                if channel == 'GENERAL':
                    price_info['import_price'] = price_data.get('perKwh')
                    price_info['import_descriptor'] = price_data.get('descriptor')
                    price_info['renewables'] = price_data.get('renewables')
                elif channel == 'FEED_IN':
                    price_info['export_price'] = price_data.get('perKwh')
                    price_info['export_descriptor'] = price_data.get('descriptor')
            
            return price_info
        except Exception as e:
            logger.error(f"Error getting price info: {e}")
            return None
    
    def decide_strategy(self, price_info: dict) -> str:
        """
        Decide the best strategy based on current prices
        
        Args:
            price_info: Current price information
            
        Returns:
            Strategy: 'charge', 'discharge', or 'normal'
        """
        import_price = price_info.get('import_price')
        export_price = price_info.get('export_price')
        import_desc = price_info.get('import_descriptor')
        export_desc = price_info.get('export_descriptor')
        
        if import_price is None:
            logger.warning("No import price available, using normal mode")
            return "normal"
        
        # Priority 1: Charge during negative or very low prices
        if import_desc == 'NEGATIVE' or import_price <= self.charge_threshold:
            logger.info(f"Low import price ({import_price:.2f} c/kWh) - Strategy: CHARGE")
            return "charge"
        
        # Priority 2: Discharge during high prices (if export price is good)
        if export_price and (export_desc in ['HIGH', 'SPIKE'] or export_price >= self.discharge_threshold):
            logger.info(f"High export price ({export_price:.2f} c/kWh) - Strategy: DISCHARGE")
            return "discharge"
        
        # Priority 3: Discharge during high import prices (avoid grid usage)
        if import_desc in ['HIGH', 'SPIKE']:
            logger.info(f"High import price ({import_price:.2f} c/kWh) - Strategy: DISCHARGE")
            return "discharge"
        
        # Default: Normal operation
        logger.info("Normal price conditions - Strategy: NORMAL")
        return "normal"
    
    def apply_strategy(self, strategy: str) -> bool:
        """
        Apply the chosen strategy to the inverter
        
        Args:
            strategy: 'charge', 'discharge', or 'normal'
            
        Returns:
            True if successful
        """
        if strategy == self.current_strategy:
            logger.debug(f"Already in {strategy} mode, no change needed")
            return True
        
        try:
            if strategy == "charge":
                success = self.inverter.force_charge()
            elif strategy == "discharge":
                success = self.inverter.force_discharge()
            else:  # normal
                success = self.inverter.set_normal_mode()
            
            if success:
                self.current_strategy = strategy
                logger.info(f"Successfully changed to {strategy} mode")
            else:
                logger.error(f"Failed to change to {strategy} mode")
            
            return success
        except Exception as e:
            logger.error(f"Error applying strategy: {e}")
            return False
    
    def run_once(self) -> dict:
        """
        Run one cycle of price check and inverter control
        
        Returns:
            Status dictionary
        """
        logger.info("=" * 60)
        logger.info("Starting control cycle")
        
        # Get current prices
        price_info = self.get_current_price_info()
        if not price_info:
            logger.error("Failed to get price information")
            return {"success": False, "error": "Failed to get prices"}
        
        logger.info(f"Import: {price_info['import_price']:.2f} c/kWh ({price_info['import_descriptor']})")
        if price_info['export_price']:
            logger.info(f"Export: {price_info['export_price']:.2f} c/kWh ({price_info['export_descriptor']})")
        logger.info(f"Renewables: {price_info['renewables']:.1f}%")
        
        # Decide strategy
        strategy = self.decide_strategy(price_info)
        
        # Apply strategy
        success = self.apply_strategy(strategy)
        
        # Get inverter status
        inverter_status = self.inverter.get_status()
        
        result = {
            "success": success,
            "timestamp": price_info['timestamp'],
            "price_info": price_info,
            "strategy": strategy,
            "inverter_status": inverter_status
        }
        
        logger.info(f"Cycle complete - Strategy: {strategy}, Success: {success}")
        return result
    
    def run_continuous(self):
        """
        Run the controller continuously
        
        Monitors prices and adjusts inverter at regular intervals
        """
        logger.info(f"Starting continuous operation (interval: {self.check_interval}s)")
        logger.info(f"Charge threshold: {self.charge_threshold} c/kWh")
        logger.info(f"Discharge threshold: {self.discharge_threshold} c/kWh")
        
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                logger.info(f"\nCycle #{cycle_count}")
                
                result = self.run_once()
                
                # Save result to log file (optional)
                self._save_log(result)
                
                logger.info(f"Sleeping for {self.check_interval} seconds...")
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("\nShutting down gracefully...")
            # Return to normal mode before exit
            self.inverter.set_normal_mode()
            logger.info("Controller stopped")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            # Try to return to normal mode
            try:
                self.inverter.set_normal_mode()
            except:
                pass
            raise
    
    def _save_log(self, result: dict):
        """Save result to JSON log file"""
        try:
            with open('inverter_control_log.json', 'a') as f:
                f.write(json.dumps(result) + '\n')
        except Exception as e:
            logger.warning(f"Failed to save log: {e}")


def main():
    """
    Main entry point
    """
    import sys
    
    # Load configuration (you should use a proper config file)
    AMBER_API_TOKEN = "your_amber_api_token_here"
    INVERTER_SERIAL = "your_inverter_serial_here"
    
    # Configuration
    CHARGE_THRESHOLD = 0.0  # Charge when price <= 0 c/kWh (negative pricing)
    DISCHARGE_THRESHOLD = 30.0  # Discharge when price >= 30 c/kWh
    CHECK_INTERVAL = 300  # 5 minutes
    
    if AMBER_API_TOKEN == "your_amber_api_token_here":
        print("ERROR: Please set your Amber API token in the configuration")
        print("Get your token from: https://app.amber.com.au/settings/")
        sys.exit(1)
    
    try:
        controller = SmartInverterController(
            amber_api_token=AMBER_API_TOKEN,
            inverter_sn=INVERTER_SERIAL,
            charge_threshold=CHARGE_THRESHOLD,
            discharge_threshold=DISCHARGE_THRESHOLD,
            check_interval=CHECK_INTERVAL
        )
        
        # Run once or continuously based on command line argument
        if len(sys.argv) > 1 and sys.argv[1] == "--once":
            result = controller.run_once()
            print(json.dumps(result, indent=2))
        else:
            controller.run_continuous()
            
    except Exception as e:
        logger.error(f"Failed to start controller: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
