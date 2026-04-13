from .aave_client import AaveClient
from .config import config
from loguru import logger

class RiskManager:
    def __init__(self):
        self.aave = AaveClient()

    async def check_and_alert(self) -> bool:
        health = await self.aave.get_health()
        
        if health['ltv'] > config.max_ltv:
            logger.warning("⚠️ LTV HIGH - Rebalancing needed")
            return False
            
        if health['health'] < config.liq_alert:
            logger.critical("🚨 LIQUIDATION ALERT <80%!")
            await self.emergency_unwind()
            return False
            
        return True

    async def emergency_unwind(self):
        """Repay all debt + withdraw collateral"""
        logger.critical("🛑 EMERGENCY UNWIND")
        # Repay logic here
