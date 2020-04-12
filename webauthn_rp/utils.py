import base64
import re
from typing import Union
from urllib.parse import urlparse

from cryptography.hazmat.primitives.hashes import (SHA256, SHA384, SHA512,
                                                   HashAlgorithm)

from webauthn_rp import types
from webauthn_rp.constants import (EC2_P_256_NUMBER_LENGTH,
                                   EC2_P_384_NUMBER_LENGTH,
                                   EC2_P_521_NUMBER_LENGTH,
                                   OKP_ED448_NUMBER_LENGTH,
                                   OKP_ED25519_NUMBER_LENGTH)
from webauthn_rp.errors import ValidationError

CURVE_COORDINATE_BYTE_LENGTHS = {
    'P_256': EC2_P_256_NUMBER_LENGTH,
    'P_384': EC2_P_384_NUMBER_LENGTH,
    'P_521': EC2_P_521_NUMBER_LENGTH,
    'ED25519': OKP_ED25519_NUMBER_LENGTH,
    'ED448': OKP_ED448_NUMBER_LENGTH,
}

EC2_HASH_ALGORITHMS = {
    'ES256': SHA256,
    'ES384': SHA384,
    'ES512': SHA512,
}


def snake_to_camel_case(s: str) -> str:
  chunks = [x for x in re.split(r'_+', s) if x]
  capped = [x[0].upper() + x[1:] for x in chunks[1:]]
  if chunks:
    return chunks[0] + ''.join(capped)
  return ''


def camel_to_snake_case(s: str) -> str:
  words = []
  s_index = 0
  for i in range(len(s)):
    if s[i].isupper():
      words.append(s[s_index:i].lower())
      s_index = i
  if s_index < len(s): words.append(s[s_index:].lower())
  return '_'.join(words)


def url_base64_encode(b: bytes) -> bytes:
  return base64.b64encode(b, b'-_')


def url_base64_decode(s: str) -> bytes:
  return base64.b64decode(s + '===', b'-_')


def extract_origin(url: str) -> str:
  parsed_url = urlparse(url)
  if parsed_url.netloc is None:
    raise ValidationError('Origin must contain hostname[:port]')

  if parsed_url.scheme is None:
    raise ValidationError('Origin must contain scheme')

  return parsed_url.scheme + '://' + parsed_url.netloc


def curve_coordinate_byte_length(
    crv: Union['types.EC2Curve.Name', 'types.EC2Curve.Value',
               'types.OKPCurve.Name', 'types.OKPCurve.Value']
) -> int:
  assert crv.name in CURVE_COORDINATE_BYTE_LENGTHS, 'Unexpected curve'
  return CURVE_COORDINATE_BYTE_LENGTHS[crv.name]


def ec2_hash_algorithm(
    alg: Union['types.COSEAlgorithmIdentifier.Name',
               'types.COSEAlgorithmIdentifier.Value']
) -> HashAlgorithm:
  assert alg.name in EC2_HASH_ALGORITHMS, 'Invalid COSE algorithm'
  return EC2_HASH_ALGORITHMS[alg.name]()
