import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.config import get_google_maps_api_key

router = APIRouter()

GOOGLE_MAPS_API_KEY = get_google_maps_api_key()


@router.get("/location")
async def get_nearby_shrines(
    latitude: float, longitude: float, radius: int = 5000
):
    """
    現在地を基に半径内の神社を取得し、距離を計算して近い順にソート
    """
    try:
        # Nearby Search APIを呼び出して神社の情報を取得
        url = (
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={latitude},{longitude}&radius={radius}&keyword=神社\
            &key={GOOGLE_MAPS_API_KEY}&language=ja&region=jp"
        )
        response = requests.get(url)
        response_data = response.json()

        # 神社情報を整理
        shrines = [
            {
                "name": result.get("name"),
                "address": result.get("vicinity"),
                "location": result.get("geometry", {}).get("location"),
            }
            for result in response_data.get("results", [])[:5]
        ]

        # 各神社までの距離を取得
        for shrine in shrines:
            shrine_location = shrine.get("location")
            if shrine_location:
                destination = f"{shrine_location['lat']},{shrine_location['lng']}"
                distance_url = (
                    "https://maps.googleapis.com/maps/api/distancematrix/json"
                    f"?origins={latitude},{longitude}&destinations={destination}&mode=walking&key={GOOGLE_MAPS_API_KEY}"
                )
                distance_response = requests.get(distance_url)
                distance_data = distance_response.json()

                # 距離データを取得して追加
                if (
                    distance_data.get("rows")
                    and distance_data["rows"][0].get("elements")
                    and distance_data["rows"][0]["elements"][0].get("distance")
                ):
                    shrine["distance"] = distance_data["rows"][0]["elements"][0]["distance"]["text"]
                    shrine["distance_value"] = distance_data["rows"][0]["elements"][0]["distance"]["value"]  # ソート用（メートル単位）
                else:
                    shrine["distance"] = "不明"
                    shrine["distance_value"] = float('inf')  # ソート用に最大値を設定

        # 距離の近い順にソート
        sorted_shrines = sorted(shrines, key=lambda x: x["distance_value"])

        return JSONResponse(content={"shrines": sorted_shrines})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
