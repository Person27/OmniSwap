from brownie import network, Contract, SoDiamond, WormholeFacet, LibSoFeeWormholeV1
import ccxt

from scripts.helpful_scripts import get_wormhole_info, get_account
from scripts.utils import aptos_brownie


def set_so_gas():
    proxy_wormhole = Contract.from_abi(
        "WormholeFacet", SoDiamond[-1].address, WormholeFacet.abi)

    nets = ["mainnet", "bsc-main", "avax-main", "polygon-main"]

    gas = get_wormhole_info()["gas"]
    for net in nets:
        if net == network.show_active():
            continue
        print(f"network:{network.show_active()}, "
              f"set dst net {net} wormhole gas: "
              f"base_gas:{gas[net]['base_gas']},"
              f"per_byte_gas:{gas[net]['per_byte_gas']}")
        proxy_wormhole.setWormholeGas(
            gas[net]["dst_chainid"],
            gas[net]["base_gas"],
            gas[net]["per_byte_gas"],
            {'from': get_account()}
        )


def set_so_price():
    api = ccxt.binance()
    symbols = ["ETH/USDT", "BNB/USDT", "MATIC/USDT", "AVAX/USDT", "APT/USDT"]
    prices = {}

    for symbol in symbols:
        result = api.fetch_ohlcv(symbol=symbol,
                                 timeframe="1m",
                                 limit=1)
        price = result[-1][4]
        print(f"Symbol:{symbol}, price:{price}")
        prices[symbol] = price

    decimal = 1e27
    multiply = 1.1
    if network.show_active() == "avax-main":
        # bnb
        dst_wormhole_id = 2
        ratio = int(prices["BNB/USDT"] / prices["AVAX/USDT"] * decimal * multiply)
        print(f"Set price ratio for bnb-main:{ratio}")
        LibSoFeeWormholeV1[-1].setPriceRatio(dst_wormhole_id,
                                             ratio, {"from": get_account()})
        # aptos
        dst_wormhole_id = 22
        ratio = int(prices["APT/USDT"] / prices["AVAX/USDT"] * decimal * multiply)
        print(f"Set price ratio for aptos-mainnet:{ratio}")
        LibSoFeeWormholeV1[-1].setPriceRatio(dst_wormhole_id,
                                             ratio, {"from": get_account()})

    if network.show_active() == "mainnet":
        # aptos
        dst_wormhole_id = 22
        ratio = int(prices["APT/USDT"] / prices["ETH/USDT"] * decimal * multiply)
        print(f"Set price ratio for aptos-mainnet:{ratio}")
        LibSoFeeWormholeV1[-1].setPriceRatio(dst_wormhole_id,
                                             ratio, {"from": get_account()})

    if network.show_active() == "polygon-main":
        # aptos
        dst_wormhole_id = 22
        ratio = int(prices["APT/USDT"] / prices["MATIC/USDT"] * decimal * multiply)
        print(f"Set price ratio for aptos-mainnet:{ratio}")
        LibSoFeeWormholeV1[-1].setPriceRatio(dst_wormhole_id,
                                             ratio, {"from": get_account()})

    if network.show_active() == "bsc-main":
        # aptos
        dst_wormhole_id = 22
        ratio = int(prices["APT/USDT"] / prices["BNB/USDT"] * decimal * multiply)
        print(f"Set price ratio for aptos-mainnet:{ratio}")
        LibSoFeeWormholeV1[-1].setPriceRatio(dst_wormhole_id,
                                             ratio, {"from": get_account()})