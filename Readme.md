aave-loop-bot/
├── src/
│   ├── __init__.py
│   ├── config.py              # Settings/Addresses
│   ├── abis.py                # Aave contracts
│   ├── aave_client.py         # Core Aave ops
│   ├── swap_router.py         # USDC → stETH
│   ├── risk_manager.py        # LTV/liquidation
│   ├── rebalancer.py          # Daily automation
│   ├── monitor.py             # Live dashboard
│   └── simulator.py           # P&L testing
├── tests/
│   ├── test_aave.py
│   ├── test_risk.py
│   └── test_loop.py
├── output/
│   └── (auto-generated CSVs)
├── requirements.txt
├── .env.example
├── docker-compose.yml
└── main.py                    # Run this!
