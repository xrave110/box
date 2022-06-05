from re import A
from matplotlib.pyplot import get
from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest


def test_proxy_updates():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_data_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_data_initializer_function,
        {"from": account},
    )

    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("Box", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    upgrade(
        account,
        proxy,
        box_v2.address,
        proxy_admin_contract=proxy_admin,
        initializer=box_encoded_data_initializer_function,
    )
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
