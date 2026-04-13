#!/usr/bin/env python3
import asyncio
import pandas as pd
from src.simulator import PnlSimulator
from src.rebalancer import DailyRebalancer
from src.monitor import start_monitoring
from loguru import logger
import os

async def main():
    os.makedirs("output", exist_ok=True)
    logger.add("output/aave_loop_{time}.log", rotation="1d")
    
    # 1. Run P&L Sim
    sim = PnlSimulator()
    df = sim.run_24_months()
    df.to_csv("output/aave_pnl.csv")
    logger.success("📊 P&L Sim complete")
    
    # 2. LIVE LOOP (toggle)
    LIVE = os.getenv("LIVE", "false").lower() == "true"
    if LIVE:
        rebalancer = DailyRebalancer()
        await rebalancer.execute_loop()
    
    # 3. Start monitoring
    await start_monitoring()

if __name__ == "__main__":
    asyncio.run(main())

