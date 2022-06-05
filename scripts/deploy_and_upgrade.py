from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    Contract,
    network,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
)


def main():
    account = get_account()
    print("Deploying to {}".format(network.show_active()))
    box = Box.deploy({"from": account})
    print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,  # implementation of smart contract address
        proxy_admin,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 10000000},
    )
    print("Proxy deployed to {}, you can now upgrade to v2".format(proxy))
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())
    # print(proxy_box.increment())

    box_v2 = BoxV2.deploy({"from": account})
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    print("Proxy has been updated")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print(proxy_box.retrieve())
    print(proxy_box.increment({"from": account}))
    print(proxy_box.retrieve())
