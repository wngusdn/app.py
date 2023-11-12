import streamlit as st
import pandas as pd
import random
import time
import os
import matplotlib.pyplot as plt

# CSV 파일명
csv_file = "user_data.csv"
matching_result_file = "matching_result.csv"

# 데이터 프레임 초기화 또는 로딩
def load_data(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame()

# 사용자 정보 및 매칭 결과 데이터 프레임
user_data = load_data(csv_file)
matching_result = load_data(matching_result_file)

# 스타일 설정
st.markdown('<p style="position: absolute; top: 10px; right: 10px; color: blue; font-size: 24px; font-weight: bold;">iOS</p>', unsafe_allow_html=True)

plt.rc('font', family='AppleGothic')  # macOS용 폰트 설정
plt.rc('font', size=15)
plt.rc('axes', unicode_minus=False)

# 사용자 정보 입력
st.title("Random Matching2")
st.markdown("#### 사용자 정보 입력(필수)")

name = st.text_input("이름")
age = st.selectbox("나이", ["고등학교 1학년", "고등학교 2학년", "고등학교 3학년"])
gender = st.selectbox("성별", ["남자", "여자"])
phone_number = st.text_input("전화번호")

# 사용자 정보 확인 및 저장
if st.button("확인"):
    if len(phone_number) == 11:
        user_data = pd.DataFrame({"이름": [name], "나이": [age], "성별": [gender], "전화번호": [phone_number]})
        user_data.to_csv(csv_file, index=False)
        st.success("정보가 성공적으로 저장되었습니다.")
    else:
        st.warning("전화번호를 11자리로 입력해주세요.")

# 사용자 정보 출력
st.markdown("### 사용자 정보")
st.dataframe(user_data)

# 랜덤 매칭 버튼
if st.button("랜덤 매칭 시작"):
    male_users = user_data[user_data['성별'] == '남자']
    female_users = user_data[user_data['성별'] == '여자']

    matching_result = pd.DataFrame(columns=['매칭 그룹', '성별', '이름'])
    
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
    
# 오류 정보 확인 버튼
if st.button("오류 정보 검사"):
    duplicates = user_data[user_data.duplicated(subset=['이름', '전화번호'], keep=False)]
    leading_space_names = user_data[user_data['이름'].str.startswith(' ')]
    
    if not duplicates.empty:
        st.subheader("중복 데이터:")
        st.dataframe(duplicates)
    
    if not leading_space_names.empty:
        st.subheader("이름 앞에 빈 칸으로 저장된 데이터:")
        st.dataframe(leading_space_names)

# 관리자 비밀번호 설정
admin_password = "jhny0403"
admin_access = 0
admin_password_input = st.sidebar.text_input("관리자 비밀번호", type="password")

if admin_password_input == admin_password:
    admin_access = 1
    st.sidebar.success("관리자 권한이 부여되었습니다.")

# 관리자 권한이 있는 경우 초기화 버튼 표시
if admin_access == 1:
    if st.sidebar.button("사용자 정보 초기화"):
        user_data = pd.DataFrame(columns=["이름", "나이", "성별", "전화번호"])
        user_data.to_csv(csv_file, index=False)
        st.sidebar.success("사용자 정보가 초기화되었습니다.")


