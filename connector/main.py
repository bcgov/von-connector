#! /usr/bin/python3

from von_agent.nodepool import NodePool

import asyncio


async def main():
    pool = NodePool('test', '.indy/pool_transactions_sandbox_genesis')

    print('\n\n\nOpening pool...\n\n\n')
    await pool.open()
    print('\n\n\nFinished opening pool\n\n\n')

    print('\n\n\nClosing pool...\n\n\n')
    await pool.close()
    print('\n\n\nFinished closing pool\n\n\n')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
