from requests import post

from wrapper_api.agent.agents import AgentRegistrar, Origin, Verifier, Issuer, Prover

import json
import logging


class TrustAnchorAgent(AgentRegistrar, Origin):
    """
    Trust anchor register agents and schemata & claim defs onto the distributed ledger
    """

    async def process_post(self, form: dict) -> str:
        """
        Takes a request from service wrapper POST and dispatches the applicable agent action.
        Returns (json) response arising from processing.

        :param form: request form on which to operate
        :return: json response
        """

        logger = logging.getLogger(__name__)
        logger.debug('TrustAnchorAgent.process_post: >>> form: {}'.format(form))

        self.__class__._vet_keys({'type', 'data'}, set(form.keys()))  # all tokens need type and data

        # Try each responder code base from BaseListeningAgent up before trying locally
        mro = TrustAnchorAgent._mro_dispatch()
        for ResponderClass in mro:
            try:
                rv = await ResponderClass.process_post(self, form)
                logger.debug('TrustAnchorAgent.process_post: <<< {}'.format(rv))
                return rv
            except NotImplementedError:
                pass

        # token-type/proxy
        logger.debug('TrustAnchorAgent.process_post: <!< not this form type: {}'.format(form['type']))
        raise NotImplementedError('{} does not support token type {}'.format(self.__class__.__name__, form['type']))


class SRIAgent(Verifier, Issuer):
    """
    SRI agent is a verifier for BC registrar claims and an issuer of SRI registration claims.
    """

    async def process_post(self, form: dict) -> str:
        """
        Takes a request from service wrapper POST and dispatches the applicable agent action.
        Returns (json) response arising from processing.

        :param form: request form on which to operate
        :return: json response
        """

        logger = logging.getLogger(__name__)
        logger.debug('SRIAgent.process_post: >>> form: {}'.format(form))

        self.__class__._vet_keys({'type', 'data'}, set(form.keys()))  # all tokens need type and data

        # Try each responder code base from BaseListeningAgent up before trying locally
        mro = SRIAgent._mro_dispatch()
        for ResponderClass in mro:
            try:
                rv = await ResponderClass.process_post(self, form)
                logger.debug('SRIAgent.process_post: <<< {}'.format(rv))
                return rv
            except NotImplementedError:
                pass

        # token-type/proxy
        logger.debug('SRIAgent.process_post: <!< not this form type: {}'.format(form['type']))
        raise NotImplementedError('{} does not support token type {}'.format(self.__class__.__name__, form['type']))


class BCRegistrarAgent(Issuer):
    """
    BC registrar agent is an issuer of BC registrar claims
    """

    async def process_post(self, form: dict) -> str:
        """
        Takes a request from service wrapper POST and dispatches the applicable agent action.
        Returns (json) response arising from processing.

        :param form: request form on which to operate
        :return: json response
        """

        logger = logging.getLogger(__name__)
        logger.debug('BCRegistrarAgent.process_post: >>> form: {}'.format(form))

        self.__class__._vet_keys({'type', 'data'}, set(form.keys()))  # all tokens need type and data

        # Try each responder code base from BaseListeningAgent up before trying locally
        mro = SRIAgent._mro_dispatch()
        for ResponderClass in mro:
            try:
                rv = await ResponderClass.process_post(self, form)
                logger.debug('BCRegistrarAgent.process_post: <<< {}'.format(rv))
                return rv
            except NotImplementedError:
                pass

        # token-type/proxy
        logger.debug('BCRegistrarAgent.process_post: <!< not this form type: {}'.format(form['type']))
        raise NotImplementedError('{} does not support token type {}'.format(self.__class__.__name__, form['type']))


class OrgBookAgent(Prover):
    """
    The Org Book  agent is a prover of BC registrar claims
    """

    async def process_post(self, form: dict) -> str:
        """
        Takes a request from service wrapper POST and dispatches the applicable agent action.
        Returns (json) response arising from processing.

        :param form: request form on which to operate
        :return: json response
        """

        logger = logging.getLogger(__name__)
        logger.debug('OrgBookAgent.process_post: >>> form: {}'.format(form))

        self.__class__._vet_keys({'type', 'data'}, set(form.keys()))  # all tokens need type and data

        # Try each responder code base from BaseListeningAgent up before trying locally
        mro = OrgBookAgent._mro_dispatch()
        for ResponderClass in mro:
            try:
                rv = await ResponderClass.process_post(self, form)
                logger.debug('OrgBookAgent.process_post: <<< {}'.format(rv))
                return rv
            except NotImplementedError:
                pass

        # token-type/proxy
        logger.debug('OrgBookAgent.process_post: <!< not this form type: {}'.format(form['type']))
        raise NotImplementedError('{} does not support token type {}'.format(self.__class__.__name__, form['type']))
