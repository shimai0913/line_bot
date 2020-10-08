# 標準モジュール
import os
import urllib.request

# pip モジュール
import xml.etree.ElementTree as ET

# 自作モジュール
import log as log


# ========================================================================== #
#  グローバル変数
# ========================================================================== #
# google_places_api_key = os.environ['GOOGLE_PLACES_API_KEY']
google_places_api_key = "AIzaSyBg0R3y6NrdzTJ1QxXmw715jjCiDndWmiw"
# google_places_api_key = os.getenv('GOOGLE_PLACES_API_KEY', None)
google_directions_api_key = "AIzaSyBg0R3y6NrdzTJ1QxXmw715jjCiDndWmiw"
# google_directions_api_key = os.getenv('GOOGLE_DIRECTIONS_API_KEY', None)
google_staticmaps_api_key = "AIzaSyBg0R3y6NrdzTJ1QxXmw715jjCiDndWmiw"
# google_staticmaps_api_key = os.getenv('GOOGLE_STATICMAPS_API_KEY', None)


# ========================================================================== #
#  関数名：get_near_station
# -------------------------------------------------------------------------- #
#  説明：現在地から最寄り駅検索
# ========================================================================== #
def get_near_station(lat, lon):
    log.print_log("get_near_station start.")

    # SimpleAPIから最寄駅リストを取得
    near_station_url = f"http://map.simpleapi.net/stationapi?x={lon}&y={lat}&output=xml"
    near_station_req = urllib.request.Request(near_station_url)
    with urllib.request.urlopen(near_station_req) as response:
        near_station_XmlData = response.read()
    near_station_root = ET.fromstring(near_station_XmlData)
    near_station_list = near_station_root.findall(".//name")

    # 最寄駅名から座標を取得
    near_station_geo_url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query={}&key={}".format(
        urllib.parse.quote_plus(near_station_list[0].text, encoding="utf-8"),
        google_places_api_key,
    )
    near_station_geo_req = urllib.request.Request(near_station_geo_url)
    with urllib.request.urlopen(near_station_geo_req) as response:
        near_station_geo_XmlData = response.read()
    near_station_geo_root = ET.fromstring(near_station_geo_XmlData)

    # 最寄駅情報(名前、住所、緯度経度)を取得
    # near_station_name = near_station_geo_root.findtext(".//name")
    # near_station_address = near_station_geo_root.findtext(".//formatted_address")
    near_station_geo_lat = near_station_geo_root.findtext(".//lat")
    near_station_geo_lon = near_station_geo_root.findtext(".//lng")

    # 徒歩時間を取得
    near_station_direction_url = f"https://maps.googleapis.com/maps/api/directions/xml?origin={lat},{lon}&destination={near_station_geo_lat},{near_station_geo_lon}&mode=walking&key={google_directions_api_key}"
    near_station_direction_req = urllib.request.Request(near_station_direction_url)
    with urllib.request.urlopen(near_station_direction_req) as response:
        near_station_direction_XmlData = response.read()

    near_station_direction_root = ET.fromstring(near_station_direction_XmlData)
    near_station_direction_time_second = int(
        near_station_direction_root.findtext(".//leg/duration/value")
    )
    near_station_direction_distance_meter = int(
        near_station_direction_root.findtext(".//leg/distance/value")
    )
    near_station_direction_time_min = near_station_direction_time_second // 60
    near_station_direction_distance_kilo = (
        near_station_direction_distance_meter // 1000
        + ((near_station_direction_distance_meter // 100) % 10) * 0.1
    )

    # img_map
    map_image_url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&size=520x520&scale=2&maptype=roadmap&key={}".format(
        lat, lon, google_staticmaps_api_key
    )
    # 赤ピン
    map_image_url += "&markers=color:{}|label:{}|{},{}".format(
        "red", "", near_station_geo_lat, near_station_geo_lon
    )
    # 青ピン
    map_image_url += "&markers=color:{}|label:{}|{},{}".format("blue", "", lat, lon)

    log.print_log("get_near_station Success.")

    return (
        map_image_url,
        near_station_list,
        near_station_direction_time_min,
        near_station_direction_distance_kilo,
    )
