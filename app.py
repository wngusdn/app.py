import streamlit as st
import pandas as pd
import random
import time
import os

# 초기 변수 설정
male_percentage = 0
female_percentage = 0
male_match_probability = 0
female_match_probability = 0

# 오른쪽 위 모서리에 텍스트 추가
st.markdown('<p style="position: absolute; top: 10px; right: 10px; color: blue; font-size: 24px; font-weight: bold;">iOS</p>', unsafe_allow_html=True)

# 사용자 정보를 저장할 CSV 파일명
csv_file = "user_data.csv"
matching_result_file = "matching_result.csv"

# 데이터 프레임 로딩 또는 초기화
if "users" not in st.session_state:
    st.session_state.users = pd.DataFrame()

if os.path.exists(csv_file):
    st.session_state.users = pd.read_csv(csv_file)

def load_matching_result():
    if os.path.exists(matching_result_file):
        return pd.read_csv(matching_result_file)
    else:
        return pd.DataFrame()

# Load matching result
matching_result = load_matching_result()

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
</style>
"""

js = """
<script>
  // JavaScript 코드는 여기에 추가할 수 있습니다.
</script>
"""

# HTML 코드로 애니메이션 텍스트 추가
st.write(f'{css}<div class="animate"><h1>Random Matching2</h1></div>{js}', unsafe_allow_html=True)

# 사용자 정보 입력
st.markdown("#### 사용자 정보 입력(필수)")
name = st.text_input("이름")
age = st.selectbox("나이", ["고등학교 1학년", "고등학교 2학년", "고등학교 3학년"])
gender = st.selectbox("성별", ["남자", "여자"])
phone_number = st.text_input("전화번호")

# 사용자 정보 저장
if st.button("확인"):
    if len(phone_number) == 11:
        user_data = pd.DataFrame({"이름": [name], "나이": [age], "성별": [gender], "전화번호": [phone_number]})
        st.session_state.users = pd.concat([st.session_state.users, user_data], ignore_index=True)

        # CSV 파일로 저장
        st.session_state.users.to_csv(csv_file, index=False)

        info_message = st.empty()
        info_message.success("정보가 성공적으로 저장되었습니다.")
        time.sleep(2)
        info_message.empty()
    else:
        st.warning("전화번호를 11자리로 입력해주세요.")

# 관리자 비밀번호 설정
admin_password = "jhny0403"
admin_access = 0

admin_password_input = st.sidebar.text_input("관리자 비밀번호", type="password")

# 올바른 관리자 비밀번호를 입력한 경우
if admin_password_input == admin_password:
    admin_access = 1

# 관리자 권한이 있는 경우에만 랜덤 매칭 버튼을 표시
if admin_access == 1:
    info_message1 = st.empty()
    info_message1.success("관리자 권한이 부여되었습니다.")
    time.sleep(2)
    info_message1.empty()

    if st.button("사용자 정보 초기화"):
        empty_data = pd.DataFrame(columns=["이름", "나이", "성별", "전화번호", "매칭그룹"])
        empty_data.to_csv(csv_file, index=False)
        empty_data1 = pd.DataFrame(columns=["이름", "전화번호", "매칭그룹"])
        empty_data1.to_csv(matching_result_file, index=False)
        st.success("사용자 정보가 초기화되었습니다.")
    
    st.markdown("###유저 데이터 검색")

    # 이름으로 검색하는 Streamlit 앱
    search_name = st.text_input("검색할 이름을 입력하세요:")

    if st.button("검색"):
        search_result = st.session_state.users[st.session_state.users['이름'] == search_name]
        if not search_result.empty:
            st.subheader(f"{search_name}에 대한 정보:")
            for idx, row in search_result.iterrows():
                st.write(f"인덱스: {idx}, 전화번호 {row['전화번호']}, 성별: {row['성별']}")
        else:
            st.write(f"{search_name}에 대한 정보를 찾을 수 없습니다.")

    # 사용자 정보 출력
    st.markdown("### 사용자 정보")
    user_data = st.session_state.users
    st.dataframe(user_data)

    # 랜덤 매칭 버튼을 클릭하여 매칭 수행
    total_users = len(user_data)
    gender_counts = user_data["성별"].value_counts()
    total_users = gender_counts.sum()

    if total_users >= 2:
        male_count = gender_counts.get("남자", 0)
        female_count = gender_counts.get("여자", 0)

        male_percentage = (male_count / total_users) * 100
        female_percentage = (female_count / total_users) * 100

        st.write(f"남자 수: {male_count}")
        st.write(f"여자 수: {female_count}")
        st.write(f"총 사용자 수: {male_count + female_count}")

        if total_users == 0:
            male_match_probability = 0
            female_match_probability = 0
        elif female_count == 0:
            male_match_probability = 100
            female_match_probability = 0
        else:
            male_percentage = male_count / total_users
            female_percentage = female_count / total_users

            if male_percentage > female_percentage:
                male_match_probability = 100
                female_match_probability = female_count / male_count * 100
            else:
                female_match_probability = 100
                male_match_probability = male_count / female_count * 100

        st.write(f"여자 매칭 성공 확률: {male_match_probability:.2f}%")
        st.write(f"남자 매칭 성공 확률: {female_match_probability:.2f}%")

    # 랜덤 매칭 버튼을 클릭하여 매칭 수행
if st.button("랜덤 매칭 시작"):
    user_data_file = 'user_data.csv'
    matching_result_file = 'matching_result.csv'

    user_data = pd.read_csv(user_data_file)
    matching_result = pd.DataFrame(columns=['매칭 그룹', '성별', '이름'])

    # 남자와 여자를 분리
    male_users = st.session_state.users[st.session_state.users['성별'] == '남자']
    female_users = st.session_state.users[st.session_state.users['성별'] == '여자']

    # 일반 매칭을 생성
    matchings = []
    while len(male_users) > 0 and len(female_users) > 0:
        male = male_users.sample(1)
        female = female_users.sample(1)
        matching = (male['이름'].values[0], female['이름'].values[0])
        matchings.append(matching)
        male_users = male_users.drop(male.index)
        female_users = female_users.drop(female.index)

    # 나머지 매칭 결과 출력
    for i, (male, female) in enumerate(matchings):
        st.text(f"매칭 그룹 {i + 1}: {male}와 {female}")

        # 매칭 결과를 matching_result에 추가
        matching_result = matching_result.append({'매칭 그룹': i + 1, '성별': '남자', '이름': male}, ignore_index=True)
        matching_result = matching_result.append({'매칭 그룹': i + 1, '성별': '여자', '이름': female}, ignore_index=True)

    # 남는 남자들을 소외된 데이터로 만들어 결과로 출력
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

                # 소외된 남자 매칭 결과를 matching_result에 추가
                matching_result = matching_result.append({'매칭 그룹': group_text, '성별': '남자', '이름': male}, ignore_index=True)

        # 홀수명의 남자는 단독으로 소외된 데이터 그룹에 추가
        if len(male_users) == 1:
            i += leftover_group_count
            group_text = f"{i + 1}"
            st.text(f"매칭 그룹 {group_text} (남자 1명):")
            st.text(male_users.iloc[0]['이름'])

            # 소외된 남자 매칭 결과를 matching_result에 추가
            matching_result = matching_result.append({'매칭 그룹': group_text, '성별': '남자', '이름': male_users.iloc[0]['이름']}, ignore_index=True)

    # CSV 파일로 저장 (matching_result에 저장)
    matching_result.to_csv(matching_result_file, index=False)
