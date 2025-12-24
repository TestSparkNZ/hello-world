# Amber Energy and GoodWe Inverter Integration Guide

## Overview

This application integrates Amber Energy's dynamic pricing API with GoodWe inverter control to optimize solar energy usage based on electricity prices.

## Amber Energy API

Amber provides real-time electricity pricing data for Australian households. The API allows you to:

### Key Features
- Get current electricity prices (per kWh)
- Get price forecasts for the next 24-48 hours
- Identify peak, off-peak, and negative price periods
- Access renewable energy percentage data

### API Endpoints

#### 1. Authentication
```
GET https://api.amber.com.au/v1/sites
Headers: Authorization: Bearer YOUR_API_TOKEN
```

#### 2. Get Current Prices
```
GET https://api.amber.com.au/v1/sites/{siteId}/prices/current
```

Response includes:
- `perKwh`: Current price in cents per kWh
- `renewables`: Percentage of renewable energy
- `channelType`: GENERAL (import) or FEED_IN (export)
- `descriptor`: NEGATIVE, LOW, NEUTRAL, HIGH, SPIKE

#### 3. Get Price Forecast
```
GET https://api.amber.com.au/v1/sites/{siteId}/prices
```

Returns hourly price forecasts for planning ahead.

### Getting Your API Token

1. Log in to https://app.amber.com.au/
2. Go to Settings > Developer Settings
3. Enable Developer Mode
4. Copy your API token

## GoodWe Inverter Integration

GoodWe inverters can be controlled through:

### Option 1: GoodWe SEMS API
- Cloud-based API for monitoring and control
- Requires registration with SEMS portal
- Supports remote start/stop operations

### Option 2: Local Modbus TCP/IP
- Direct communication over local network
- Faster response, no internet required
- Requires network-enabled inverter models

### Control Operations
- **Start**: Enable inverter operation
- **Stop/Standby**: Put inverter in standby mode
- **Force Charge**: Charge battery from grid
- **Force Discharge**: Discharge battery to grid

## Use Cases

### 1. Price-Based Battery Control
When electricity prices are:
- **Negative or Very Low**: Charge battery from grid, run inverter
- **High or Spike**: Discharge battery to grid, optimize export
- **Normal**: Standard solar operation

### 2. Grid Support
During high renewable periods (low prices), support grid by consuming excess energy.

### 3. Cost Optimization
Automatically manage battery charge/discharge cycles to minimize electricity costs.

## Safety Considerations

⚠️ **Important Safety Notes:**
- Never disable inverter safety features
- Ensure battery limits are respected
- Monitor inverter temperature and status
- Have manual override capability
- Test thoroughly before deployment
- Comply with local grid regulations

## Technical Requirements

- Python 3.8+
- Network connectivity (for Amber API)
- GoodWe inverter with network capability
- Valid Amber Energy account with API access

## References

- Amber API Documentation: https://app.amber.com.au/developers
- GoodWe SEMS Portal: https://www.semsportal.com
- GoodWe Modbus Documentation: Contact GoodWe support
