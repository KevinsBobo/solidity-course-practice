from ecdsa import SigningKey, SECP256k1
import sha3


def checksum_encode(addr_str):  # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out


def test(addrstr):
    assert(addrstr == checksum_encode(addrstr))


def generate_wallet():
    keccak = sha3.keccak_256()

    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak.update(pub)
    address = keccak.hexdigest()[24:]

    print("Private key:", priv.to_string().hex())
    print("Public key: ", pub.hex())
    print("Address:    ", checksum_encode(address))


if __name__ == "__main__":
    generate_wallet()
