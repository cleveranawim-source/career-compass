# AI 시대 미래진로 검사도구

직업 하나를 정답처럼 고르는 대신, **진로 가설과 다음 행동**을 찾도록 돕는 중·고등학생용 자기검사 2종입니다.

**바로 쓰기:** https://cleveranawim-source.github.io/career-compass/

| 도구 | 문항 · 시간 | 결과 |
|---|---|---|
| 🧭 [미래진로 나침반](https://cleveranawim-source.github.io/career-compass/compass.html) | 63문항 · 15~20분 | 끌리는 활동 조합(RIASEC), 일 가치, 진로적응·탐색 행동·AI 협업 단계, 30일 작은 실험 |
| 🔭 [계획된 우연 기회발견 자기검사](https://cleveranawim-source.github.io/career-compass/happenstance.html) | 25문항 · 7~10분 | 호기심·끈기·유연성·낙관성·작은 위험 감수 프로필, 7일 실천 미션, 우연 포착 일지 |

- 회원가입·서버 전송이 없습니다. 응답은 브라우저 탭 안(sessionStorage)에만 잠시 보관되고 탭을 닫으면 사라집니다.
- 결과는 학생이 직접 복사(패들렛 붙여넣기용)·텍스트 저장·인쇄합니다. 결과 화면이 아닌 곳에서 인쇄하면 지필용 문항지가 나옵니다.
- **표준화된 심리검사가 아닙니다.** 연구·수업용 프로토타입이므로 선발·배치·입시 판단·진단에 사용할 수 없습니다.

운영 방법, 이론적 근거, 금지 사용, 타당화 로드맵은 [학교 활용 및 타당화 가이드(PDF)](guide.pdf)에 있습니다.

## 파일

- `index.html`, `compass.html`, `happenstance.html` — 각각 한 파일로 완결된 페이지(빌드 없음). 파일만 내려받아 열어도 작동합니다.
- `guide.md` → `guide.pdf` — `tools/build_guide_pdf.py`로 생성합니다(markdown, pypdf, reportlab, Chrome 필요).

버전을 올릴 때는 세 HTML의 하단 표기와 `VERSION` 상수, `guide.md` 변경 기록을 함께 고칩니다.
