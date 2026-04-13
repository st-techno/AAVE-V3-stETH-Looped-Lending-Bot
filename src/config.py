import os
from dataclasses import dataclass
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()

@dataclass
class Config:
    rpc_url: str = os.getenv("RPC_URL")
    private_key: str = os.getenv("PRIVATE_KEY")
    initial_steth: int = int(os.getenv("INITIAL_STETH", Web3.to_wei(100_000 / 3500, 'ether')))  # ~$100K
    max_ltv: float = float(os.getenv("MAX_LTV", 0.67))  # 67% for 150% LTV
    liq_alert: float = float(os.getenv("LIQ_ALERT", 0.80))
    rebalance_hour: int = int(os.getenv("REBALANCE_HOUR", 2))

# Aave V3 Mainnet (2026 verified)
ADDRESSES = {
    'AAVE_POOL': '0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2',
    'STETH': '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84',
    'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'WETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    'UNISWAP_V3': '0xE592427A0AEce92De3Edee1F18E0157C05861564',  # SwapRouter
    'CHAINLINK_ETH_USD': '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'
}

config = Config()

