from binascii import hexlify, unhexlify
from math import ceil, log

import json


def ppjson(dumpit):
    """
    JSON pretty printer, whether already json-encoded or not
    """

    return json.dumps(json.loads(dumpit) if isinstance(dumpit, str) else dumpit, indent=4)

def encode(value):
    """
    Encoder for claim values, returns encoded value.
    Operation leaves any (stringified) int32 alone: indy-sdk predicate claims operate on int32
    values properly only when their encoded values match their raw values.

    To disambiguate for decoding, the function adds 2**32 to any non-trivial transform.
    """

    s = str(value)
    try:
        i = int(value)
        if 0 <= i < 2**32:  # it's an i32, leave it (as numeric string)
            return s
    except (ValueError, TypeError):
        pass

    return str(int.from_bytes(hexlify(s.encode()), 'big') + 2**32)


def decode(value: str):
    """
    Decoder for encoded claim values, returns decoded value.

    :param value: numeric string to decode
    """

    assert value.isdigit()

    if 0 <= int(value) < 2**32:  # it's an i32, leave it (as numeric string)
        return value

    i = int(value) - 2**32
    blen = ceil(log(i, 16)/2)
    ibytes = unhexlify(i.to_bytes(blen, 'big'))
    return ibytes.decode()


def plain_claims_for(claims: dict, filt: dict = {}) -> dict:
    """
    Find claims matching input attribute-value dict from within input claims structure,
    json-loaded as returned via agent get_claims().
    
    The input claims holds claims with values encoded to numeric strings as per
    encode() above; this utility chooses only those matching the input original
    (non-encoded) value, replacing any values for attributes in the filter with their
    respective plain (non-encoded) values for more cogent display.

    :param claims: claims structure via get_claims();
        e.g., {
            "attrs": {
                "attr0_uuid": [
                    {
                        "claim_uuid": "claim::00000000-0000-0000-0000-000000000000",
                        "attrs": {
                            "attr0": "2",
                            "attr1": "8080189724314",
                            "attr2": "110838914834142413139418734819234123943712834123947912834701743281470"
                        },
                        "issuer_did": "Q4zqM7aXqm7gDQkUVLng9h",
                        "schema_seq_no": 21
                    },
                    {
                        "claim_uuid": "claim::00000000-0000-0000-0000-111111111111",
                        "attrs": {
                            "attr0": "1",
                            "attr1": "8080189724314",
                            "attr2": "1"
                        },
                        "issuer_did": "Q4zqM7aXqm7gDQkUVLng9h",
                        "schema_seq_no": 21
                    }
                ],
                "attr1_uuid": [
                    {
                        "claim_uuid": "claim::00000000-0000-0000-0000-000000000000",
                        "attrs": {
                            "attr0": "2",
                            "attr1": "8080189724314",
                            "attr2": "110838914834142413139418734819234123943712834123947912834701743281470"
                        },
                        "issuer_did": "Q4zqM7aXqm7gDQkUVLng9h",
                        "schema_seq_no": 21
                    },
                    {
                        "claim_uuid": "claim::00000000-0000-0000-0000-111111111111",
                        "attrs": {
                            "attr0": "1",
                            "attr1": "8080189724314",
                            "attr2": "1"
                        },
                        "issuer_did": "Q4zqM7aXqm7gDQkUVLng9h",
                        "schema_seq_no": 21
                    }
                ],
                "attr2_uuid": [
                    {
                        "claim_uuid": "claim::00000000-0000-0000-0000-000000000000",
                        "attrs": {
                            "attr0": "2",
                            "attr1": "8080189724314",
                            "attr2": "110838914834142413139418734819234123943712834123947912834701743281470"
                        },
                        "issuer_did": "Q4zqM7aXqm7gDQkUVLng9h",
                        "schema_seq_no": 21
                    },
                    {
                        "claim_uuid": "claim::00000000-0000-0000-0000-111111111111",
                        "attrs": {
                            "attr0": "1",
                            "attr1": "8080189724314",
                            "attr2": "1"
                        },
                        "issuer_did": "Q4zqM7aXqm7gDQkUVLng9h",
                        "schema_seq_no": 21
                    }
                ]
            }
        }
    :param filt: attributes and values to match from claims structure
    :return: dict mapping claim uuid to claim attributes for claims matching input filter. This returned structure
        is suitable for display and human inference, not for re-use in further protocol operations, since it
        presents any filter attributes as plain, pre-encoding values that the indy-sdk does not recognize.
    """

    uuid2claims = claims['attrs']
    encfilt = {k: encode(filt[k]) for k in filt}
    matches = {}
    for claims in uuid2claims.values():
        for claim in claims:
            if claim['claim_uuid'] not in matches and (encfilt.items() <= claim['attrs'].items()):
                matches[claim['claim_uuid']] = {
                    k: filt[k] if k in filt else decode(claim['attrs'][k])
                    for k in claim['attrs']
                }

    return matches


def prune_claims_json(claim_uuids: set, claims: dict) -> str:
    """
    Strips all claims out of the input json structure that do not match any of the input claim uuids

    :param claim_uuids: the set of claim uuids, as specified in claims json structure returned from get_claims,
        showing up as dict keys that claims_for_value() returns
    :param claims: claims structure returned by get_claims()
    :return: the reduced claims json
    """

    for attr_uuid, claims_by_uuid in claims['attrs'].items():
        claims['attrs'][attr_uuid] = [claim for claim in claims_by_uuid if claim['claim_uuid'] in claim_uuids]

    return json.dumps(claims)
