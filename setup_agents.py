#! /usr/bin/python3

import sys
import os
import json

import asyncio

from pprint import pprint
from indy import pool


async def main():
    await pool.create_pool_ledger_config('test', json.dumps({'genesis_txn': './indy/pool_transactions_sandbox_genesis'}))
    connection = await pool.open_pool_ledger('test', None)
    pprint(connection)
    await pool.close_pool_ledger(connection)
    await pool.delete_pool_ledger_config('test')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
