from indy import pool, signus, wallet, IndyError
from indy.error import ErrorCode

import json
import logging


class Wallet:
    """
    Class encapsulating indy-sdk wallet.
    """

    def __init__(self, pool_name: str, seed: str, base_name: str, num: int = 0, cfg_json: str = None) -> None:
        """
        Initializer for wallet. Stores input parameters and creates wallet.
        Does not open until open() or __enter__().

        :param pool_name: name of pool on which wallet operates
        :param seed: seed for wallet user
        :param base_name: base name of the wallet (indy-sdk wallet name will take a dot and a number as a suffix)
        :param num: suffix number for wallet name
        :param cfg_json: wallet configuration json, None for default
        """

        logger = logging.getLogger(__name__)
        logger.debug('Wallet.__init__: >>> pool_name {}, seed [SEED], base_name {}, num {}, cfg_json {}'.format(
            pool_name,
            base_name,
            num,
            cfg_json))

        self._pool_name = pool_name
        self._seed = seed
        self._base_name = base_name
        try:
            self._num = int(num) 
        except ValueError:
            logger.error('Wallet.__init__: input num {} is not an int, using 0'.format(num))
            self._num = 0
        self._handle = None
        self._cfg_json = cfg_json

        self._did = None
        self._verkey = None
        self._pubkey = None

        logger.debug('Wallet.__init__: <<<')

    @property
    def pool_name(self) -> str:
        """
        Accessor for pool name

        :return: pool name
        """

        return self._pool_name

    @property
    def base_name(self) -> str:
        """
        Accessor for wallet base name

        :return: wallet base name
        """

        return self._base_name

    @property
    def name(self) -> str:
        """
        Accessor for wallet (full) name

        :return: wallet (full) name
        """

        return '{}.{}'.format(self._base_name, self._num)

    @property
    def num(self) -> int:
        """
        Accessor for wallet suffix number

        :return: wallet suffix number
        """

        return self._num

    @property
    def handle(self) -> int:
        """
        Accessor for indy-sdk pool handle

        :return: indy-sdk pool handle
        """

        return self._handle

    @property
    def cfg_json(self) -> str:
        """
        Accessor for wallet config json

        :return: wallet config json
        """

        return self._cfg_json

    @property
    def did(self) -> str:
        """
        Accessor for wallet DID

        :return: wallet DID
        """

        return self._did

    @property
    def verkey(self) -> str:
        """
        Accessor for wallet verification key

        :return: wallet verification key
        """

        return self._verkey

    @property
    def pubkey(self) -> str:
        """
        Accessor for wallet public (encryption) key

        :return: wallet public (encryption) key
        """

        return self._pubkey

    async def __aenter__(self) -> 'Wallet':
        """
        Context manager entry. Creates and opens wallet as configured, for closure on context manager exit.
        For use in monolithic call opening, using, and closing wallet.

        :return: current object
        """

        logger = logging.getLogger(__name__)
        logger.debug('Wallet.__aenter__: >>>')

        rv = await self.open()
        logger.debug('Wallet.__aenter__: <<<')
        return rv

    async def open(self) -> 'Wallet':
        """
        Explicit entry. Opens wallet as configured, for later closure via close().
        For use when keeping wallet open across multiple calls.

        :return: current object
        """

        logger = logging.getLogger(__name__)
        logger.debug('Wallet.open: >>>')

        while True:
            try:
                await wallet.create_wallet(
                    pool_name=self.pool_name,
                    name=self.name,
                    xtype=None,
                    config=self.cfg_json,
                    credentials=None)
                break
            except IndyError as e:
                if e.error_code == ErrorCode.WalletAlreadyExistsError:
                    logger.info('Wallet.open: wallet {} already exists, incrementing ...')
                    self._num += 1
                    continue
                else:
                    raise

        self._handle = await wallet.open_wallet(self.name, self.cfg_json, None)
        logger.info('Wallet.open: created and opened wallet {} on handle {}'.format(self.name, self.num))

        (self._did, self._verkey, self._pubkey) = (
            await signus.create_and_store_my_did(self._handle, json.dumps({'seed': self._seed})))
        logger.info('Wallet.open: stored {}, {}, {}'.format(self._did, self._verkey, self._pubkey))

        logger.debug('Wallet.open: <<<')
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None: 
        """
        Context manager exit. Closes and deletes wallet.
        For use in monolithic call opening, using, and closing the pool.

        :param exc_type:
        :param exc:
        :param traceback:
        """

        logger = logging.getLogger(__name__)
        logger.debug('Wallet.__aexit__: >>>')

        await self.close()

        logger.debug('Wallet.__aexit__: <<<')

    async def close(self) -> None:
        """
        Explicit exit. Closes and deletes wallet.
        For use when keeping pool open across multiple calls.
        """

        logger = logging.getLogger(__name__)
        logger.debug('Wallet.close: >>>')

        await wallet.close_wallet(self.handle)
        await wallet.delete_wallet(self.name, None)

        logger.debug('Wallet.close: <<<')

    def __repr__(self) -> str:
        """
        Return representation for current object.

        :return: representation for current object
        """

        return '{}({}, [SEED], {}, {}, {})'.format(
            self.__class__.__name__,
            self.pool_name,
            self.base_name,
            self.num,
            self.cfg_json)
