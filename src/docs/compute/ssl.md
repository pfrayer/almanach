---
description: "OpenSSL TLS/SSL cheatsheet: debug certificates, check expiry, verify chains, generate keys and list ciphers."
---

# TLS & SSL

## Mozilla SSL Configuration Generator

[https://ssl-config.mozilla.org/](https://ssl-config.mozilla.org/){target=_blank}

## Debug certificates

### Inspect a local certificate

```shell
openssl x509 -in cert.pem -text -noout
```

Key fields to look for: `Issuer`, `Subject`, `Validity`, `Subject Alternative Name`, `Key Usage`.

### Inspect a remote certificate

```shell
# Basic — dumps the full TLS handshake and certificate chain
openssl s_client -connect example.com:443 </dev/null

# Show only the leaf certificate details
openssl s_client -connect example.com:443 </dev/null 2>/dev/null \
  | openssl x509 -text -noout

# Use SNI (required for virtual-hosted servers)
openssl s_client -connect example.com:443 -servername example.com </dev/null
```

### Check expiry date

```shell
# Local file
openssl x509 -in cert.pem -noout -dates

# Remote — print expiry date only
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate
```

### Verify a certificate chain

```shell
# Verify cert against a CA bundle
openssl verify -CAfile ca.pem cert.pem

# Verify a full chain (intermediate + root)
openssl verify -CAfile root.pem -untrusted intermediate.pem cert.pem

# Verify against the system CA store
openssl verify cert.pem
```

### Check that a certificate, key, and CSR match

The modulus (or public key hash) must be identical across all three.

```shell
openssl x509 -noout -modulus -in cert.pem   | openssl md5
openssl rsa  -noout -modulus -in key.pem    | openssl md5
openssl req  -noout -modulus -in csr.pem    | openssl md5
```

### Test a TLS connection and cipher

```shell
# List supported ciphers for a server
openssl s_client -connect example.com:443 -cipher 'ALL' </dev/null 2>&1 | grep Cipher

# Force a specific TLS version
openssl s_client -connect example.com:443 -tls1_2 </dev/null
openssl s_client -connect example.com:443 -tls1_3 </dev/null
```

---

## Keys

### Generate an RSA private key

```shell
# 4096-bit key (recommended for RSA)
openssl genrsa -out key.pem 4096

# With AES-256 passphrase protection
openssl genrsa -aes256 -out key.pem 4096
```

### Generate an ECDSA private key

```shell
# P-256 curve (good default, widely supported)
openssl ecparam -name prime256v1 -genkey -noout -out key.pem

# P-384 curve (stronger)
openssl ecparam -name secp384r1 -genkey -noout -out key.pem

# List available curves
openssl ecparam -list_curves
```

### Extract the public key from a private key

```shell
# From RSA key
openssl rsa -in key.pem -pubout -out pub.pem

# From EC key
openssl ec -in key.pem -pubout -out pub.pem
```

### Inspect a key

```shell
# RSA key details (modulus, exponents, primes)
openssl rsa -in key.pem -text -noout

# EC key details (curve, coordinates)
openssl ec -in key.pem -text -noout

# Public key only
openssl pkey -in pub.pem -pubin -text -noout
```

### Remove passphrase from a key

```shell
openssl rsa -in key-encrypted.pem -out key.pem
```

### Add/change passphrase on a key

```shell
openssl rsa -aes256 -in key.pem -out key-encrypted.pem
```

### Sign and verify data

```shell
# Sign a file
openssl dgst -sha256 -sign key.pem -out signature.bin file.txt

# Verify signature
openssl dgst -sha256 -verify pub.pem -signature signature.bin file.txt
```

---

## Certificates and CA

### Generate a self-signed certificate

```shell
# Key + self-signed cert in one command (dev/testing only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/C=FR/ST=IDF/L=Paris/O=Acme/CN=example.com"
```

!!! warning
    Self-signed certificates are not trusted by browsers or clients by default.
    Use a proper CA for anything beyond local testing.

### Generate a CSR (Certificate Signing Request)

```shell
# With an existing key
openssl req -new -key key.pem -out csr.pem \
  -subj "/C=FR/ST=IDF/L=Paris/O=Acme/CN=example.com"

# Generate key + CSR in one step
openssl req -newkey rsa:4096 -nodes -keyout key.pem -out csr.pem \
  -subj "/C=FR/ST=IDF/L=Paris/O=Acme/CN=example.com"

# Inspect the CSR
openssl req -in csr.pem -text -noout
```

### Generate a CSR with Subject Alternative Names (SANs)

```shell
openssl req -new -key key.pem -out csr.pem \
  -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:www.example.com,DNS:*.example.com"
```

### Create a Root CA

```shell
# 1. Generate the CA private key
openssl genrsa -aes256 -out ca.key 4096

# 2. Generate the self-signed CA certificate (valid 10 years)
openssl req -x509 -new -nodes -key ca.key \
  -sha256 -days 3650 -out ca.crt \
  -subj "/C=FR/O=Acme CA/CN=Acme Root CA"
```

### Sign a CSR with your CA

```shell
openssl x509 -req -in csr.pem \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out cert.pem -days 825 -sha256
```

### Sign a CSR with SANs preserved

SANs from the CSR are not copied automatically — use an extensions file:

```shell
# ext.cnf
cat > ext.cnf <<EOF
[v3_req]
subjectAltName = DNS:example.com, DNS:www.example.com
EOF

openssl x509 -req -in csr.pem \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out cert.pem -days 825 -sha256 \
  -extfile ext.cnf -extensions v3_req
```

### Create an Intermediate CA

```shell
# 1. Generate intermediate key + CSR
openssl genrsa -aes256 -out intermediate.key 4096
openssl req -new -key intermediate.key -out intermediate.csr \
  -subj "/C=FR/O=Acme CA/CN=Acme Intermediate CA"

# 2. Sign with root CA, adding CA:TRUE constraint
cat > intermediate_ext.cnf <<EOF
[v3_ca]
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints=critical,CA:true,pathlen:0
keyUsage=critical,digitalSignature,cRLSign,keyCertSign
EOF

openssl x509 -req -in intermediate.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out intermediate.crt -days 1825 -sha256 \
  -extfile intermediate_ext.cnf -extensions v3_ca
```

---

## Format conversions

### PEM ↔ DER

```shell
# PEM → DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER → PEM
openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem
```

### PEM → PKCS#12 (`.p12` / `.pfx`)

```shell
# Bundle cert + key + CA chain into a PKCS#12 file
openssl pkcs12 -export \
  -out bundle.p12 \
  -inkey key.pem \
  -in cert.pem \
  -certfile ca.crt
```

### PKCS#12 → PEM

```shell
# Extract everything (cert + key + CA chain)
openssl pkcs12 -in bundle.p12 -out bundle.pem -nodes

# Extract only the certificate
openssl pkcs12 -in bundle.p12 -nokeys -out cert.pem

# Extract only the private key
openssl pkcs12 -in bundle.p12 -nocerts -nodes -out key.pem
```
