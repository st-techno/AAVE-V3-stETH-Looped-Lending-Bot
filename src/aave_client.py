import asyncio
from web3 import Web3
from eth_account.signers.local import LocalAccount
from tenacity import retry
from loguru import logger
from .config import config, ADDRESSES, AAVE_POOL_ABI
from .web3_client import ProdWeb3  # See below

class AaveClient:
    def __init__(self):
        self.w3 = ProdWeb3().w3
        self.account: LocalAccount = ProdWeb3().get_account()
        self.pool = self.w3.eth.contract(address=ADDRESSES['AAVE_POOL'], abi=AAVE_POOL_ABI)
        self.usdc = self.w3.eth.contract(address=ADDRESSES['USDC'], abi=USDC_ABI)

    @retry
    async def supply_steth(self, amount: int):
        """Deposit stETH as collateral"""
        tx = self.pool.functions.supply(
            ADDRESSES['STETH'], amount, self.account.address, 0
        ).build_transaction(self._base_tx())
        receipt = await self._send_tx(tx)
        logger.success(f"✅ Supplied {amount/1e18:.2f} stETH")
        return receipt

    @retry
    async def borrow_usdc(self, amount: int):
        """Borrow 50% USDC (<4% rate)"""
        tx = self.pool.functions.borrow(
            ADDRESSES['USDC'], amount, 2, 0  # Variable rate
        ).build_transaction(self._base_tx())
        receipt = await self._send_tx(tx)
        logger.success(f"✅ Borrowed {amount/1e6:.0f} USDC")
        return receipt

    async def get_health(self) -> dict:
        """Current LTV/Health Factor"""
        data = self.pool.functions.getUserAccountData(self.account.address).call()
        ltv = data[4] / 1e18  # Current LTV
        health = data[5] / 1e18
        logger.info(f"Health: {health:.2f} | LTV: {ltv:.1%}")
        return {'ltv': ltv, 'health': health}

    def _base_tx(self):
        return {
            'from': self.account.address,
            'gas': 300000,
            'gasPrice': self.w3.to_wei('25', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(self.account.address)
        }

    async def _send_tx(self, tx):
        signed = self.account.sign_transaction(tx)
        hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return self.w3.eth.wait_for_transaction_receipt(hash)

  
