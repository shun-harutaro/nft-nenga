from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

PINATA_API_KEY=os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY=os.getenv("PINATA_SECRET_API_KEY")
PINATA_BASE_URL ="https://api.pinata.cloud/pinning/pinFileToIPFS"

# Pinataへのアップロード関数
async def upload_to_pinata(upload_file: UploadFile):
    try:

        file_content = await upload_file.read()
        # ヘッダーを設定
        headers = {
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_API_KEY,
        }

        # ファイルデータを送信
        files = {"file": (upload_file.filename, file_content)}
        response = requests.post(PINATA_BASE_URL, headers=headers, files=files)

        # レスポンスを処理
        if response.status_code == 200:
            response_data = response.json()
            ipfs_hash = response_data["IpfsHash"]
            return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        else: 
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file: {response.text}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
    
async def get_nft_image(nft_id: str):
    pass
