'''
実際には実行しない、わかりやすくここに置いておきます。
このファイルを実行することでHackuNFT_abi.jsonとHackuNFT_bytecode.jsonが生成されます。
'''
from solcx import compile_standard, install_solc
import json
import os

# Solidityコンパイラのバージョンをインストール
install_solc("0.8.20")

# Solidityコードを記載
solidity_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./node_modules/@openzeppelin/contracts/token/ERC721/extensions//ERC721URIStorage.sol";
import "./node_modules/@openzeppelin/contracts/access/Ownable.sol";

contract HackuNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;

    constructor(address initialOwner) ERC721("HackuNFT", "HNFT") Ownable(initialOwner) {
        tokenCounter = 0;
    }

    function createNFT(string memory tokenURI) public onlyOwner returns (uint256) {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter += 1;
        return newTokenId;
    }
}
"""

# Solidityコードをコンパイル
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"HackuNFT.sol": {"content": solidity_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.20",  # Solidityバージョンを指定
    allow_paths=os.path.abspath("node_modules")  # OpenZeppelinのパスを許可
)

# デバッグ用出力
print(json.dumps(compiled_sol, indent=4))

# コンパイル結果をファイルに保存
output_dir = "./compiled"
os.makedirs(output_dir, exist_ok=True)

# ABIを保存
try:
    abi = compiled_sol["contracts"]["HackuNFT.sol"]["HackuNFT"]["abi"]
    with open(os.path.join(output_dir, "HackuNFT_abi.json"), "w") as abi_file:
        json.dump(abi, abi_file, indent=4)

    # バイトコードを保存
    bytecode = compiled_sol["contracts"]["HackuNFT.sol"]["HackuNFT"]["evm"]["bytecode"]["object"]
    with open(os.path.join(output_dir, "HackuNFT_bytecode.json"), "w") as bytecode_file:
        json.dump({"bytecode": bytecode}, bytecode_file, indent=4)

    print("コンパイル完了")
    print(f"ABI: {output_dir}/HackuNFT_abi.json")
    print(f"バイトコード: {output_dir}/HackuNFT_bytecode.json")
except KeyError as e:
    print(f"KeyError: {e}")
    print("コンパイル結果を再確認してください。")
