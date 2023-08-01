"""Run importers and reconcile data, using the beancount-import framework
   (https://github.com/jbms/beancount-import)."""

import glob
import os
import json
import sys
from typing import List
from magicbeans import config
from magicbeans.importers.chiawallet import ChiaWalletImporter
from magicbeans.importers.coinbase import CoinbaseImporter
from magicbeans.importers.coinbasepro import CoinbaseProImporter
from magicbeans.importers.gateio import GateIOImporter
import beangulp
from beangulp.importer import Importer

def get_importers() -> List[Importer]:
   importers = []

   # TODO: move these arguments to a config file
   importers.append(CoinbaseImporter(
      account_root="Assets:Coinbase",
      account_gains="Income:PnL",
      account_fees="Expenses:Financial:Fees",))

   importers.append(ChiaWalletImporter(
      account_root="Assets:ChiaWallet",
      account_mining_income="Income:Mining",
      account_gains="Income:PnL",
      account_fees="Expenses:Financial:Fees",))

   importers.append(GateIOImporter(
      account_root="Assets:GateIO",
      account_pnl="Income:PnL",
      account_fees="Expenses:Financial:Fees",))

   importers.append(CoinbaseProImporter(
      account_root="Assets:Coinbase",
      account_pnl="Income:PnL",
      account_fees="Expenses:Financial:Fees",))

   return importers

if __name__ == '__main__':
    importers = get_importers()
    hooks = [config.cbp_filter_xfer_hook,
             config.chiawallet_filter_xfer_hook,
             config.cbp_tweak_xfer_timestamp_hook,
             ]
    cli = beangulp.Ingest(importers, hooks).cli
    cli()