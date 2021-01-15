# ElGamal
Encrypt and Decrypt text with ElGamal cryptsystem

# Overview
ElGamal暗号を使ってテキスト文を暗号化かつ復号化するプログラムです。
公開鍵や秘密鍵を生成する機能もついています。
素人の習作なので実際に使うと危険ですのでお気をつけください。

# Usage
python ElGamal.py [-h] [-e message] [-d encrypted_message] [-p public_key] [-s secret_key] [-m]

## オプションの説明
### -h
ヘルプメッセージを出力する。

### -e message
message を暗号化する。

### -d encrypted_message
暗号化されたencrypted_messageを復号化する。

### -p public_key
暗号化、復号化に用いる公開鍵のファイルを指定する。

### -s secret_key
暗号化、復号化に用いる秘密鍵のファイルを指定する。

### -m
公開鍵のファイル、秘密鍵のファイルを作成する。

# Requirement
python3.8.5以上

# Lisence
MIT Lisence
