# 공인중개사 문제 이미지 준비 가이드

## 📁 파일명 규칙

```
questions/YYYY_C_T_NN.png

YYYY: 년도 (2025, 2024, 2023...)
C: 차수 (1=1차, 2=2차)
T: 교시 (1=1교시, 2=2교시)
NN: 문제번호 (01-40, 앞에 0 붙이기)
```

## 📋 예시

### 2025년 제36회

**1차 1교시 (부동산학개론 + 민법)**
- `questions/2025_1_1_01.png` ~ `questions/2025_1_1_40.png` (부동산학개론)
- `questions/2025_1_1_41.png` ~ `questions/2025_1_1_80.png` (민법)

**2차 1교시 (공인중개사법 + 부동산공법)**
- `questions/2025_2_1_01.png` ~ `questions/2025_2_1_40.png` (공인중개사법)
- `questions/2025_2_1_41.png` ~ `questions/2025_2_1_80.png` (부동산공법)

**2차 2교시 (부동산공시법 및 세법)**
- `questions/2025_2_2_01.png` ~ `questions/2025_2_2_40.png`

## 🖼️ 이미지 캡처 방법

### 방법 1: 맥북 스크린샷 (추천)

1. PDF 열기
2. 각 문제를 **Cmd + Shift + 4**로 캡처
3. 캡처 영역: 문제 번호 + 문제 내용 + 5개 선택지 전체
4. 파일명 변경: `2025_1_1_01.png`

### 방법 2: PDF → PNG 자동 변환

```bash
# ImageMagick 설치 (없다면)
brew install imagemagick

# PDF를 PNG로 변환
cd ~/realestateagent_test
convert -density 150 -quality 90 2025년_제36회_공인중개사_1차_1교시_문제지.pdf questions/temp_%03d.png

# 파일명 일괄 변경
# (수동으로 또는 스크립트 작성)
```

### 방법 3: 온라인 도구 사용

- https://www.ilovepdf.com/pdf_to_jpg
- PDF 업로드 → JPG/PNG 다운로드
- 각 페이지를 문제별로 자르기

## 📦 폴더 구조

```
realestateagent_test/
├── realtor_image_based.html
├── manifest.json
├── sw.js
└── questions/
    ├── 2025_1_1_01.png
    ├── 2025_1_1_02.png
    ├── 2025_1_1_03.png
    ...
    ├── 2025_2_2_40.png
    ├── 2024_1_1_01.png
    ...
```

## ✂️ 이미지 자르기 팁

### 캡처 영역 예시:
```
┌──────────────────────────────────┐
│ 1. 다음에서 설명하고 있는...     │  ← 문제 번호 + 내용
│                                  │
│ ○ 최유효이용의 근거가 된다.      │  ← 선택지 시작
│ ○ 시대 또는 지가를...           │
│ ○ 토지이용을 집약하시킨다.       │
│ ○ 분리적으로 생산할 수 없다.     │
│                                  │
│ ① 부증성  ② 인접성  ③ 개별성   │  ← 답안 번호
│ ④ 영속성  ⑤ 적재성              │
└──────────────────────────────────┘
```

## 🎯 우선순위

### 1단계: 테스트용 (필수)
- `questions/2025_1_1_01.png` (첫 문제만)
- 앱 작동 테스트용

### 2단계: 2025년 완성 (120문제)
- 2025_1_1_01.png ~ 2025_1_1_80.png (80문제)
- 2025_2_1_01.png ~ 2025_2_1_80.png (80문제)
- 2025_2_2_01.png ~ 2025_2_2_40.png (40문제)
- **총 120문제**

### 3단계: 나머지 년도 추가
- 2024년, 2023년, 2022년...

## 🚀 Git 업로드

```bash
cd ~/realestateagent_test

# questions 폴더 생성
mkdir -p questions

# 이미지 파일 추가 (Finder에서 드래그 앤 드롭)

# Git에 추가
git add questions/
git add realtor_image_based.html
git commit -m "Add: 이미지 기반 문제집 + 2025년 문제 이미지"
git push origin main
```

## 📊 정답 데이터 추가

이미지를 모두 준비한 후, `realtor_image_based.html` 파일의 `questionDatabase` 배열에 데이터 추가:

```javascript
{ 
    year: 2025, 
    subject: 'intro',  // intro, civil, broker, public, disclosure
    image: 'questions/2025_1_1_01.png', 
    correct: 0,  // 정답 (0=1번, 1=2번, 2=3번, 3=4번, 4=5번)
    explanation: '해설 내용...' 
},
```

## ⚡ 빠른 시작

1. **지금**: 첫 문제 1개만 캡처해서 테스트
2. **확인**: 아이패드에서 제대로 보이는지 확인
3. **진행**: 문제없으면 나머지 119문제 추가

---

**팁**: 이미지 크기는 가로 800-1000px 정도가 적당합니다. 너무 크면 로딩이 느려지고, 너무 작으면 글씨가 안 보입니다.