# 국내 공휴일 데이터 조회 가이드

본 문서는 공공데이터포털에서 제공하는 국내 공휴일 Open API를 이용하여
연·월별 공휴일 데이터를 조회하는 방법을 정리한 문서입니다.

---

## 1. API 개요

- 제공처: 공공데이터포털 (한국천문연구원)
- 서비스명: 특일 정보 (공휴일 / 국경일 / 기념일)
- 인증 방식: Service Key (API Key)
- 응답 형식: JSON / XML (JSON 권장)
- 상업용 서비스 및 앱 사용 가능

---

## 2. API 엔드포인트

GET https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo

---

## 3. 요청 파라미터

- serviceKey (필수): 공공데이터포털에서 발급받은 인증키
- solYear (필수): 조회 연도 (예: 2025)
- solMonth (선택): 조회 월 (01 ~ 12)
- numOfRows (선택): 결과 개수 (권장: 30 ~ 50)
- pageNo (선택): 페이지 번호
- _type (선택): 응답 포맷 (json 권장)

---

## 4. 요청 예시

월 단위 공휴일 조회 예시

GET https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo
?serviceKey=YOUR_SERVICE_KEY
&solYear=2025
&solMonth=01
&numOfRows=30
&_type=json

---

## 5. 응답 예시 (JSON)

{
  "response": {
    "body": {
      "items": {
        "item": [
          {
            "dateName": "설날",
            "locdate": 20250129,
            "isHoliday": "Y"
          }
        ]
      }
    }
  }
}

---

## 6. 주요 필드 설명

- dateName: 공휴일 명칭
- locdate: 날짜 (YYYYMMDD 형식)
- isHoliday: 공휴일 여부 (Y / N)

---

## 7. 데이터 처리 규칙

- isHoliday 값이 Y 인 데이터만 공휴일로 처리
- locdate 값은 Date 타입으로 변환하여 사용
- 연 단위 또는 월 단위 캐싱 권장

---

## 8. 권장 아키텍처

공공데이터 API
 → Backend 서버 (연/월 단위 호출)
 → DB 저장 및 캐싱
 → 앱/웹 클라이언트 조회

클라이언트에서 직접 API 호출은 API Key 노출 위험으로 권장하지 않음

---

## 9. 활용 예시

- 이번 달 공휴일 조회
- 다음 공휴일까지 D-Day 계산
- 연차 사용 시 연휴 계산
- 근무일 / 급여 계산 서비스

---

## 10. 참고 사항

- API 호출 제한 존재 → 캐싱 필수
- 공휴일 정책 변경 시 데이터 갱신 필요
- 공공데이터 이용 약관 준수

