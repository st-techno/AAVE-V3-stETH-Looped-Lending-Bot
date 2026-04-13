import asyncio
from datetime import datetime
from .aave_client import AaveClient
from .swap_router import SwapRouter
from .risk_manager import RiskManager
from loguru import logger

class DailyRebalancer:
    def __init__(self):
        self.aave = AaveClient()
        self.swap = SwapRouter()
        self.risk = RiskManager()

    async def execute_loop(self):
        """Core Strategy: Supply → Borrow → Swap → Repeat"""
        if not await self.risk.check_and_alert():
            return
            
        # 1. Ensure full collateral supplied
        steth_bal = await self.aave.get_steth_balance()
        await self.aave.supply_steth(steth_bal)
        
        # 2. Borrow 50% USDC
        borrow_amt = int(steth_bal * config.max_ltv * 0.5)  # Conservative
        await self.aave.borrow_usdc(borrow_amt)
        
        # 3. Swap USDC → stETH
        await self.swap.usdc_to_steth(borrow_amt)
        
        logger.success("✅ Loop complete | 8%+ amplified yield")

    async def daily_cron(self):
        """Runs at 2AM IST daily"""
        while True:
            now = datetime.now()
            if now.hour == config.rebalance_hour:
                await self.execute_loop()
                logger.info("Daily rebalance complete")
            
            await asyncio.sleep(3600)  # 1hr check

