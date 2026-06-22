import streamlit as st
import pandas as pd
import plotly.express as px
import os

# إعدادات الصفحة العامة
st.set_page_config(page_title="LOUD-Style Free Fire Analytics", page_icon="🎮", layout="wide")

# اسم ملف تخزين البيانات
DATA_FILE = "ff_matches_data.csv"

# دالة لتحميل البيانات السابقة أو إنشاء جدول جديد إذا لم يكن موجوداً
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Tournament", "Map", "Rank", 
            "P1_Name", "P1_Kills", "P1_Damage",
            "P2_Name", "P2_Kills", "P2_Damage",
            "P3_Name", "P3_Kills", "P3_Damage",
            "P4_Name", "P4_Kills", "P4_Damage"
        ])

# تحميل البيانات في ذاكرة الموقع
if 'df' not in st.session_state:
    st.session_state.df = load_data()

st.title("🎮 لوحة تحليل أداء السكواد الاحترافي | eSports Dashboard")
st.markdown("---")

# تقسيم الشاشة إلى جزأين: اليمين لإدخال البيانات، واليسار لعرض التحليلات
col_form, col_charts = st.columns([1, 2])

# ---------------- الجزء الأول: إدخال البيانات ----------------
with col_form:
    st.header("📝 تسجيل بيانات جيم جديد")
    with st.form("match_form", clear_on_submit=True):
        tournament = st.text_input("اسم البطولة / الـ Scrim", "Scrim_Daily")
        map_name = st.selectbox("الخريطة", ["Bermuda", "Purgatory", "Kalahari", "Nexterra"])
        rank = st.number_input("ترتيب السكواد في الجيم (Rank)", min_value=1, max_value=12, value=1)
        
        st.markdown("**📊 أداء اللاعبين الأربعة:**")
        
        # بيانات اللاعب 1
        p1_n = st.text_input("اللاعب 1 (الاسم)", "Player_1")
        c1, c2 = st.columns(2)
        p1_k = c1.number_input("كيلات اللاعب 1", min_value=0, value=0, key="p1k")
        p1_d = c2.number_input("ضرر اللاعب 1", min_value=0, value=0, key="p1d")
        
        # بيانات اللاعب 2
        p2_n = st.text_input("اللاعب 2 (الاسم)", "Player_2")
        c3, c4 = st.columns(2)
        p2_k = c3.number_input("كيلات اللاعب 2", min_value=0, value=0, key="p2k")
        p2_d = c4.number_input("ضرر اللاعب 2", min_value=0, value=0, key="p2d")
        
        # بيانات اللاعب 3
        p3_n = st.text_input("اللاعب 3 (الاسم)", "Player_3")
        c5, c6 = st.columns(2)
        p3_k = c5.number_input("كيلات اللاعب 3", min_value=0, value=0, key="p3k")
        p3_d = c6.number_input("ضرر اللاعب 3", min_value=0, value=0, key="p3d")
        
        # بيانات اللاعب 4
        p4_n = st.text_input("اللاعب 4 (الاسم)", "Player_4")
        c7, c8 = st.columns(2)
        p4_k = c7.number_input("كيلات اللاعب 4", min_value=0, value=0, key="p4k")
        p4_d = c8.number_input("ضرر اللاعب 4", min_value=0, value=0, key="p4d")
        
        submit_button = st.form_submit_button("حفظ وتحديث البيانات 🚀")
        
        if submit_button:
            new_data = {
                "Tournament": tournament, "Map": map_name, "Rank": rank,
                "P1_Name": p1_n, "P1_Kills": p1_k, "P1_Damage": p1_d,
                "P2_Name": p2_n, "P2_Kills": p2_k, "P2_Damage": p2_d,
                "P3_Name": p3_n, "P3_Kills": p3_k, "P3_Damage": p3_d,
                "P4_Name": p4_n, "P4_Kills": p4_k, "P4_Damage": p4_d
            }
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
            st.session_state.df.to_csv(DATA_FILE, index=False)
            st.success("تم تسجيل الجيم بنجاح وتحديث الرسوم البيانية!")

# ---------------- الجزء الثاني: عرض التحليلات والرسوم البيانية ----------------
with col_charts:
    st.header("📊 التحليلات التلقائية والـ Analytics")
    
    if st.session_state.df.empty:
        st.info("قم بإدخال أول مباراة من القائمة الجانبية لتظهر لك الرسوم البيانية هنا.")
    else:
        df = st.session_state.df
        
        # حساب إحصائيات عامة
        total_matches = len(df)
        avg_rank = round(df["Rank"].mean(), 1)
        total_kills = df[["P1_Kills", "P2_Kills", "P3_Kills", "P4_Kills"]].sum().sum()
        
        # عرض بطاقات رقمية علوية (KPIs)
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="عدد المباريات المسجلة", value=total_matches)
        kpi2.metric(label="متوسط ترتيب السكواد", value=avg_rank, help="كلما اقترب من 1 كان الأداء أفضل")
        kpi3.metric(label="إجمالي كيلات السكواد", value=total_matches)
        
        st.markdown("---")
        
        # معالجة البيانات لإظهار أداء كل لاعب على حدة
        player_stats = pd.DataFrame([
            {"اللاعب": df["P1_Name"].iloc[-1], "الكيلات": df["P1_Kills"].sum(), "الضرر": df["P1_Damage"].sum()},
            {"اللاعب": df["P2_Name"].iloc[-1], "الكيلات": df["P2_Kills"].sum(), "الضرر": df["P2_Damage"].sum()},
            {"اللاعب": df["P3_Name"].iloc[-1], "الكيلات": df["P3_Kills"].sum(), "الضرر": df["P3_Damage"].sum()},
            {"اللاعب": df["P4_Name"].iloc[-1], "الكيلات": df["P4_Kills"].sum(), "الضرر": df["P4_Damage"].sum()},
        ])
        
        # رسم بياني لتوزيع الكيلات بين اللاعبين (Pie Chart)
        ch1, ch2 = st.columns(2)
        
        with ch1:
            st.subheader("🎯 نسبة مساهمة اللاعبين في الكيلات")
            fig_kills = px.pie(player_stats, values="الكيلات", names="اللاعب", hole=0.4, 
                               color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_kills, use_container_width=True)
            
        with ch2:
            st.subheader("🔥 مقارنة إجمالي الضرر (Damage)")
            fig_dmg = px.bar(player_stats, x="اللاعب", y="الضرر", text_auto=True,
                             color="الضرر", color_continuous_scale="Viridis")
            st.plotly_chart(fig_dmg, use_container_width=True)
            
        st.markdown("---")
        
        # تتبع أداء السكواد حسب الخريطة
        st.subheader("🗺️ متوسط ترتيب السكواد حسب الخريطة")
        map_perf = df.groupby("Map")["Rank"].mean().reset_index()
        fig_map = px.line(map_perf, x="Map", y="Rank", markers=True, 
                          labels={"Rank": "متوسط الترتيب (الأقل أفضل)"})
        # عكس المحور Y لأن المركز الأول (1) هو الأفضل
        fig_map.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_map, use_container_width=True)
        
        # عرض الجدول الخام أسفل الصفحة
        st.subheader("📋 سجل المباريات التفصيلي")
        st.dataframe(df, use_container_width=True)
