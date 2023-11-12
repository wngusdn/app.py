import streamlit as st
import pandas as pd
import random
import time
import os

# CSS 코드
css = """
<style>
  .animate {
    animation: zoom 3s infinite;
  }
  @keyframes zoom {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      transform: scale(1);
    }
  }
</style>
"""

# 사용자 정보를 저장할 CSV 파일명
csv_file = "user_data.csv"
matching_result_file = "matching_result.csv"

# 데이터 프레임 로딩 또는 초기화 함수
def load_user_data(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame()

# 오른쪽 위 모서리에 텍스트 추가
st.markdown('<p style="position: absolute; top: 10px; right: 10px; color: blue; font-size: 24px; font-weight: bold;">iOS</p>', unsafe_allow_html=True)

# HTML 코드로 애니메이션 텍스트 추가
st.write(f'{css}<div class="animate"><h1>Random Matching2</h1></div>', unsafe_allow_html=True)

# 데이터 프레임 로딩 또는 초기화
user_data = load_user_data(csv_file)
matching_result = load_user_data(matching_result_file)

# 사용자 정보 입력
st.markdown("#### 사용자 정보 입력(필수)")
name = st.text_input("이름")
age = st.selectbox("나이", ["고등학교 1학년", "고등학교 2학년", "고등학교 3학년"])
gender = st.selectbox("성별", ["남자", "여자"])
phone_number = st.text_input("전화번호")

# 관리자 비밀번호 설정
admin_password = "jhny0403"
admin_access = 0

# CSS 및 JavaScript 코드
css = """
<style>
  .animate {
    animation: zoom 3s infinite;
  }
  @keyframes zoom {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      transform: scale(1);
    }
  }
</style>
"""

# HTML 코드로 애니메이션 텍스트 추가
st.write(f'{css}<div class="animate"><h1>Random Matching2</h1></div>', unsafe_allow_html=True)

# 관리자 권한 확인
admin_password_input = st.sidebar.text_input("관리자 비밀번호", type="password")

if admin_password_input == admin_password:
    admin_access = 1

# 관리자 권한이 있는 경우에만 랜덤 매칭 버튼을 표시
if admin_access == 1:
    st.sidebar.success("관리자 권한이 부여되었습니다.")
    if st.sidebar.button("사용자 정보 초기화"):
        user_data = pd.DataFrame(columns=["이름", "나이", "성별", "전화번호"])
        matching_result = pd.DataFrame(columns=["매칭 그룹", "성별", "이름"])
        user_data.to_csv(csv_file, index=False)
        matching_result.to_csv(matching_result_file, index=False)
        st.sidebar.success("사용자 정보가 초기화되었습니다.")

# Streamlit 앱 생성
st.title("유저 데이터 검색")

# 이름으로 검색하는 Streamlit 앱
search_name = st.text_input("검색할 이름을 입력하세요:")

if st.button("검색"):
    search_result = user_data[user_data['이름'] == search_name]
    if not search_result.empty:
        st.subheader(f"{search_name}에 대한 정보:")
        st.dataframe(search_result)
    else:
        st.write(f"{search_name}에 대한 정보를 찾을 수 없습니다.")

# 사용자 정보 출력
st.markdown("### 사용자 정보")
st.dataframe(user_data)

# 랜덤 매칭 버튼을 클릭하여 매칭 수행
if st.button("랜덤 매칭 시작"):
    # 사용자 정보 파일 로드
    user_data = load_user_data(csv_file)
    matching_result = pd.DataFrame(columns=["매칭 그룹", "성별", "이름"])
    
    male_users = user_data[user_data['성별'] == '남자']
    female_users = user_data[user_data['성별'] == '여자']

    matchings = []

    while len(male_users) > 0 and len(female_users) > 0:
        male = male_users.sample(1)
        female = female_users.sample(1)
        matching = (male['이름'].values[0], female['이름'].values[0])
        matchings.append(matching)
        male_users = male_users.drop(male.index)
        female_users = female_users.drop(female.index)

    for i, (male, female) in enumerate(matchings):
        st.text(f"매칭 그룹 {i + 1}: {male}와 {female}")
        matching_result = pd.concat([matching_result, pd.DataFrame({'매칭 그룹': [i + 1], '성별': ['남자'], '이름': [male]}), pd.DataFrame({'매칭 그룹': [i + 1], '성별': ['여자'], '이름': [female]})], ignore_index=True)

    leftover_male_count = len(male_users)

    if leftover_male_count > 0:
        st.write(f"{leftover_male_count}명의 남자가 소외되었습니다.")
        leftover_group_count = leftover_male_count // 2
        i = len(matchings)

        for group in range(leftover_group_count):
            group_text = f"{i + group + 1}"
            group_males = male_users.sample(2)
            male_users = male_users.drop(group_males.index)
            
            st.text(f"매칭 그룹 {group_text} (남자 2명):")
            for male in group_males['이름']:
                st.text(male)

            matching_result = pd.concat([matching_result, pd.DataFrame({'매칭 그룹': [group_text], '성별': ['남자'], '이름': group_males['이름'].tolist()})], ignore_index=True)

        if len(male_users) == 1:
            i += leftover_group_count
            group_text = f"{i + 1}"
            st.text(f"매칭 그룹 {group_text} (남자 1명):")
            st.text(male_users.iloc[0]['이름'])

            matching_result = pd.concat([matching_result, pd.DataFrame({'매칭 그룹': [group_text], '성별': ['남자'], '이름': [male_users.iloc[0]['이름']]})], ignore_index=True)

    matching_result.to_csv(matching_result_file, index=False)


