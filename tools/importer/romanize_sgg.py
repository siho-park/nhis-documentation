"""Add English names for the SGG district code list to tools/translations.tsv.

Usage: python romanize_sgg.py <nsc_ir.json> <translations.tsv>

Names follow the official Revised Romanization spellings used by each local
government ("Jongno-gu, Seoul"; "Suwon-si Jangan-gu, Gyeonggi-do").
"""

import json
import pathlib
import sys

PROVINCE = {
    "서울특별시": "Seoul", "부산광역시": "Busan", "대구광역시": "Daegu",
    "인천광역시": "Incheon", "광주광역시": "Gwangju", "대전광역시": "Daejeon",
    "울산광역시": "Ulsan", "세종특별자치시": "Sejong", "경기도": "Gyeonggi-do",
    "강원도": "Gangwon-do", "충청북도": "Chungcheongbuk-do",
    "충청남도": "Chungcheongnam-do", "전라북도": "Jeollabuk-do",
    "전라남도": "Jeollanam-do", "경상북도": "Gyeongsangbuk-do",
    "경상남도": "Gyeongsangnam-do", "제주도": "Jeju-do",
    "제주특별자치도": "Jeju", "강원특별자치도": "Gangwon",
    "전북특별자치도": "Jeonbuk",
}

# Romanized stems; the suffix (시 -si, 군 -gun, 구 -gu) is added in code.
STEM = dict(item.split("=") for item in """
종로=Jongno 중=Jung 용산=Yongsan 성동=Seongdong 광진=Gwangjin 동대문=Dongdaemun
중랑=Jungnang 성북=Seongbuk 강북=Gangbuk 도봉=Dobong 노원=Nowon 은평=Eunpyeong
서대문=Seodaemun 마포=Mapo 양천=Yangcheon 강서=Gangseo 구로=Guro 금천=Geumcheon
영등포=Yeongdeungpo 동작=Dongjak 관악=Gwanak 서초=Seocho 강남=Gangnam 송파=Songpa
강동=Gangdong 서=Seo 동=Dong 영도=Yeongdo 부산진=Busanjin 동래=Dongnae 남=Nam
북=Buk 해운대=Haeundae 사하=Saha 금정=Geumjeong 연제=Yeonje 수영=Suyeong
사상=Sasang 기장=Gijang 수성=Suseong 달서=Dalseo 달성=Dalseong 군위=Gunwi
미추홀=Michuhol 연수=Yeonsu 남동=Namdong 부평=Bupyeong 계양=Gyeyang 강화=Ganghwa
옹진=Ongjin 광산=Gwangsan 유성=Yuseong 대덕=Daedeok 울주=Ulju 수원=Suwon
장안=Jangan 권선=Gwonseon 팔달=Paldal 영통=Yeongtong 성남=Seongnam 수정=Sujeong
중원=Jungwon 분당=Bundang 의정부=Uijeongbu 안양=Anyang 만안=Manan 동안=Dongan
부천=Bucheon 원미=Wonmi 소사=Sosa 오정=Ojeong 광명=Gwangmyeong 평택=Pyeongtaek
동두천=Dongducheon 안산=Ansan 상록=Sangnok 단원=Danwon 고양=Goyang 덕양=Deogyang
일산=Ilsan 일산동=Ilsandong 일산서=Ilsanseo 과천=Gwacheon 구리=Guri
남양주=Namyangju 오산=Osan 시흥=Siheung 군포=Gunpo 의왕=Uiwang 하남=Hanam
용인=Yongin 처인=Cheoin 기흥=Giheung 수지=Suji 파주=Paju 이천=Icheon 안성=Anseong
김포=Gimpo 화성=Hwaseong 광주=Gwangju 양주=Yangju 포천=Pocheon 여주=Yeoju
연천=Yeoncheon 가평=Gapyeong 양평=Yangpyeong 춘천=Chuncheon 원주=Wonju
강릉=Gangneung 동해=Donghae 태백=Taebaek 속초=Sokcho 삼척=Samcheok
홍천=Hongcheon 횡성=Hoengseong 영월=Yeongwol 평창=Pyeongchang 정선=Jeongseon
철원=Cheorwon 화천=Hwacheon 양구=Yanggu 인제=Inje 고성=Goseong 양양=Yangyang
청주=Cheongju 상당=Sangdang 서원=Seowon 흥덕=Heungdeok 청원=Cheongwon
충주=Chungju 제천=Jecheon 보은=Boeun 옥천=Okcheon 영동=Yeongdong
증평=Jeungpyeong 진천=Jincheon 괴산=Goesan 음성=Eumseong 단양=Danyang
천안=Cheonan 동남=Dongnam 서북=Seobuk 공주=Gongju 보령=Boryeong 아산=Asan
서산=Seosan 논산=Nonsan 계룡=Gyeryong 당진=Dangjin 금산=Geumsan 연기=Yeongi
부여=Buyeo 서천=Seocheon 청양=Cheongyang 홍성=Hongseong 예산=Yesan 태안=Taean
전주=Jeonju 완산=Wansan 덕진=Deokjin 군산=Gunsan 익산=Iksan 정읍=Jeongeup
남원=Namwon 김제=Gimje 완주=Wanju 진안=Jinan 무주=Muju 장수=Jangsu 임실=Imsil
순창=Sunchang 고창=Gochang 부안=Buan 목포=Mokpo 여수=Yeosu 순천=Suncheon
나주=Naju 광양=Gwangyang 담양=Damyang 곡성=Gokseong 구례=Gurye 고흥=Goheung
보성=Boseong 화순=Hwasun 장흥=Jangheung 강진=Gangjin 해남=Haenam 영암=Yeongam
무안=Muan 함평=Hampyeong 영광=Yeonggwang 장성=Jangseong 완도=Wando 진도=Jindo
신안=Sinan 포항=Pohang 경주=Gyeongju 김천=Gimcheon 안동=Andong 구미=Gumi
영주=Yeongju 영천=Yeongcheon 상주=Sangju 문경=Mungyeong 경산=Gyeongsan
의성=Uiseong 청송=Cheongsong 영양=Yeongyang 영덕=Yeongdeok 청도=Cheongdo
고령=Goryeong 성주=Seongju 칠곡=Chilgok 예천=Yecheon 봉화=Bonghwa 울진=Uljin
울릉=Ulleung 창원=Changwon 의창=Uichang 성산=Seongsan 마산합포=Masanhappo
마산회원=Masanhoewon 진해=Jinhae 마산=Masan 진주=Jinju 통영=Tongyeong
사천=Sacheon 김해=Gimhae 밀양=Miryang 거제=Geoje 양산=Yangsan 의령=Uiryeong
함안=Haman 창녕=Changnyeong 남해=Namhae 하동=Hadong 산청=Sancheong
함양=Hamyang 거창=Geochang 합천=Hapcheon 제주=Jeju 서귀포=Seogwipo
북제주=Bukjeju 남제주=Namjeju
""".split())

SUFFIX = {"시": "-si", "군": "-gun", "구": "-gu"}


def unit(name):
    """'종로구' -> 'Jongno-gu'; '부천시소사구' -> 'Bucheon-si Sosa-gu'."""
    if "시" in name[:-1] and name.endswith("구") and not name.startswith("시"):
        i = name.index("시")
        if name[:i] in STEM and name[i + 1:-1] in STEM:
            return f"{unit(name[:i + 1])} {unit(name[i + 1:])}"
    return STEM[name[:-1]] + SUFFIX[name[-1]]


def english(label):
    prov, *rest = label.split()
    if prov == "세종특별자치시":
        return "Sejong"
    return f"{' '.join(unit(r) for r in rest)}, {PROVINCE[prov]}"


def main():
    ir_path, tr_path = map(pathlib.Path, sys.argv[1:3])
    ir = json.loads(ir_path.read_text(encoding="utf-8"))
    rows = dict(line.split("\t", 1)
                for line in tr_path.read_text(encoding="utf-8").splitlines() if "\t" in line)
    n = 0
    for entry in ir["code_lists"]["SGG"]:
        ko = entry["label_ko"]
        if ko not in rows:
            n += 1
        rows[ko] = english(ko)
    tr_path.write_text("\n".join(f"{k}\t{v}" for k, v in sorted(rows.items())) + "\n",
                       encoding="utf-8")
    print(f"added {n}")


if __name__ == "__main__":
    main()
