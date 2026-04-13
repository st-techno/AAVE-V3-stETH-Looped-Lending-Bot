from web3 import Web3
from .config import ADDRESSES, UNISWAP_ABI

class SwapRouter:
    def __init__(self, w3: Web3, account):
        self.w3 = w3
        self.account = account
        self.router = self.w3.eth.contract(address=ADDRESSES['UNISWAP_V3'], abi=UNISWAP_ABI)

    async def usdc_to_steth(self, usdc_amount: int, min_out: int = 0):
        """USDC → stETH Uniswap V3"""
        params = (
            ADDRESSES['USDC'],      # tokenIn
            ADDRESSES['STETH'],     # tokenOut  
            500,                    # 0.05% fee
            self.account.address,   # recipient
            int(time.time()) + 1800, # deadline 30min
            usdc_amount,            # amountIn
            min_out,                # slippage protection
            0                       # no price limit
        )
        
        # Approve USDC first
        approve_tx = self.usdc.functions.approve(ADDRESSES['UNISWAP_V3'], usdc_amount).build_transaction(...)
        # Swap TX
        swap_tx = self.router.functions.exactInputSingle(params).build_transaction(...)
        
        return await self._send_bundle([approve_tx, swap_tx])

  
