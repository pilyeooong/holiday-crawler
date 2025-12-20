"""
국내 공휴일 데이터 크롤러
공공데이터포털 API를 활용하여 공휴일 정보를 조회하고 JSON으로 저장
"""

import requests
import json
from datetime import datetime
from pathlib import Path


API_KEY = "YOUR_DATA_GO_KR_SERVICE_KEY"
BASE_URL = "https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"


def fetch_holidays(year: int, month: int = None) -> list:
    """
    공휴일 데이터 조회

    Args:
        year: 조회 연도 (예: 2025)
        month: 조회 월 (1-12), None이면 연간 전체 조회

    Returns:
        공휴일 목록 (isHoliday가 'Y'인 항목만)
    """
    params = {
        "serviceKey": API_KEY,
        "solYear": str(year),
        "numOfRows": 50,
        "pageNo": 1,
        "_type": "json"
    }

    if month:
        params["solMonth"] = str(month).zfill(2)

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get("response", {}).get("body", {}).get("items", {})

        if not items:
            return []

        item_list = items.get("item", [])

        # 단일 항목인 경우 리스트로 변환
        if isinstance(item_list, dict):
            item_list = [item_list]

        # isHoliday가 'Y'인 항목만 필터링
        holidays = [
            {
                "dateName": item.get("dateName"),
                "locdate": item.get("locdate"),
                "date": format_date(item.get("locdate")),
                "isHoliday": item.get("isHoliday")
            }
            for item in item_list
            if item.get("isHoliday") == "Y"
        ]

        return holidays

    except requests.RequestException as e:
        print(f"API 요청 오류: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return []


def format_date(locdate: int) -> str:
    """YYYYMMDD 형식을 YYYY-MM-DD로 변환"""
    if not locdate:
        return ""
    date_str = str(locdate)
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"


def fetch_year_holidays(year: int) -> list:
    """
    특정 연도의 전체 공휴일 조회 (월별로 조회하여 병합)

    Args:
        year: 조회 연도

    Returns:
        해당 연도의 전체 공휴일 목록
    """
    all_holidays = []

    for month in range(1, 13):
        print(f"{year}년 {month}월 조회 중...")
        holidays = fetch_holidays(year, month)
        all_holidays.extend(holidays)

    # 날짜순 정렬 및 중복 제거
    seen = set()
    unique_holidays = []
    for h in sorted(all_holidays, key=lambda x: x["locdate"]):
        if h["locdate"] not in seen:
            seen.add(h["locdate"])
            unique_holidays.append(h)

    return unique_holidays


def save_to_json(data: list, filename: str):
    """JSON 파일로 저장"""
    output = {
        "fetchedAt": datetime.now().isoformat(),
        "totalCount": len(data),
        "holidays": data
    }

    filepath = Path(__file__).parent / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {filepath}")
    return filepath


def main():
    """메인 실행 함수"""
    years = [2025, 2026]

    for year in years:
        print(f"\n=== {year}년 공휴일 데이터 크롤링 시작 ===\n")

        holidays = fetch_year_holidays(year)

        if holidays:
            print(f"\n총 {len(holidays)}개 공휴일 조회 완료\n")

            for h in holidays:
                print(f"  - {h['date']} : {h['dateName']}")

            save_to_json(holidays, f"holidays_{year}.json")
        else:
            print(f"{year}년 조회된 공휴일이 없습니다.")


if __name__ == "__main__":
    main()
