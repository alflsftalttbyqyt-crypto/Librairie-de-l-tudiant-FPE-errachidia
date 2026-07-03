import streamlit as st
import pandas as pd
import os
import base64

# إعداد الصفحة
st.set_page_config(page_title="المكتبة الذكية - الراشيدية", layout="wide")

# الرابط المباشر للتحميل
SHEETS_URL = "https://docs.google.com/spreadsheets/d/1oBDLx7XpHFh9JHz-kUxak4PMaAVEBC9Os22TFg7CAIo/export?format=csv"

@st.cache_data(ttl=60) # تم تقليل وقت الكاش إلى 60 ثانية لتحديث البيانات بشكل شبه لحظي للطلبة
def load_data():
    # جلب البيانات من جوجل شيت
    data = pd.read_csv(SHEETS_URL)
    
    # تحويل القيم الفارغة إلى نصوص فارغة لتجنب أخطاء (NaN)
    data = data.fillna("")
    
    # تنظيف المسافات الزائدة من بدايات ونهايات الكلمات في كل الأعمدة تلقائياً لمنع أخطاء التطابق
    for col in data.columns:
        data[col] = data[col].astype(str).str.strip()
        
    return data

# --- نظام الدخول الأكاديمي المعدل والصارم ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if not st.session_state.logged_in:
    # دالة قراءة الصورة كخلفية وتنسيق واجهة الدخول
    def add_bg_and_styling(image_file):
        if os.path.exists(image_file):
            with open(image_file, "rb") as file:
                encoded_string = base64.b64encode(file.read()).decode()
            st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            * {{ direction: rtl; }}
            .block-container {{
                background-color: rgba(235, 225, 200, 0.95);
                border: 3px solid #6b4c1a;
                border-radius: 15px;
                padding: 40px;
                margin-top: 50px;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.7);
                max-width: 600px;
            }}
            .stButton>button {{
                background-color: #4a3615;
                color: white;
                border-radius: 10px;
                border: 2px solid #2d4373;
                width: 100%;
                font-weight: bold;
                font-size: 18px;
                transition: 0.3s;
            }}
            .stButton>button:hover {{
                background-color: #6b4c1a;
                border-color: #bba14f;
            }}
            .email-suffix {{
                margin-top: 35px; 
                font-weight: bold; 
                color: #333;
                font-size: 16px;
            }}
            
            /* --- أكواد التجاوب مع شاشات الهواتف (لواجهة الدخول) --- */
            @media (max-width: 768px) {{
                .block-container {{
                    padding: 20px !important;
                    margin-top: 20px !important;
                    width: 95% !important;
                }}
                h2 {{
                    font-size: 1.5em !important;
                }}
                .email-suffix {{
                    margin-top: 5px !important;
                    text-align: center;
                    font-size: 14px;
                    margin-bottom: 15px;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True
            )

    # استدعاء الخلفية والتصميم
    add_bg_and_styling('bg.png')

    st.markdown("<h2 style='text-align: center; color: #4a3615;'>🎓 بوابة الدخول الموحدة - لطلبة الرشيدية</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b4c1a;'>Unified Entrance Portal - for Students of Errachidia</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        email_prefix = st.text_input("البريد الأكاديمي:", placeholder="يجب أن ينتهي بـ @edu.umi.ac.ma")
    with col2:
        st.markdown("<div class='email-suffix'>@edu.umi.ac.ma</div>", unsafe_allow_html=True)
    
    password = st.text_input("كلمة السر:", type="password", placeholder="أدخل كلمة المرور هنا...")
    
    st.write("---")
    
    # التوجيه للتواصل عبر فيسبوك
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px; padding: 10px;">
            لإضافة مواد أو كتب جديدة، يرجى التواصل معي عبر فيسبوك:<br>
            <a href="https://www.facebook.com/profile.php?id=100093495249631" target="_blank" style="font-weight: bold; color: #0056b3; text-decoration: none; font-size: 16px;">🔗 LAHCEN OUKHOUAOU</a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("دخول"):
        if email_prefix and email_prefix.endswith("@edu.umi.ac.ma"):
            if password == "admin2024":
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.rerun()
            elif password == "fpe2024":
                st.session_state.logged_in = True
                st.session_state.is_admin = False
                st.rerun()
            else:
                st.error("❌ كلمة السر غير صحيحة!")
        else:
            st.error("❌ عذراً، يجب أن ينتهي البريد الأكاديمي بـ @edu.umi.ac.ma")
    st.stop()

# --- التنسيق الجمالي (CSS) للمكتبة ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');
        
        .header-container { display: flex; justify-content: space-between; align-items: center; margin-top: -50px; margin-bottom: 30px; }
        .uthmani-text { font-family: 'Amiri', serif; font-size: 1.1em; color: #333; text-align: right; }
        .pray-text { margin-right: 50px; }
        .brand-text { font-size: 1.5em; font-weight: bold; color: #bba14f; }
        
        div[data-testid="stSelectbox"]:has(input[aria-label*="الشعبة"]) div[data-baseweb="select"] { border: 2px solid #2ecc71 !important; border-radius: 8px !important; }
        div[data-testid="stSelectbox"]:has(input[aria-label*="الفصل"]) div[data-baseweb="select"] { border: 2px solid #f1c40f !important; border-radius: 8px !important; }
        div[data-testid="stExpander"] { background-color: #f1c40f !important; border: none; }
        
        .welcome-box { background: linear-gradient(135deg, #bba14f, #d4af37); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
    </style>
""", unsafe_allow_html=True)

# --- الهيدر ---
st.markdown("""
    <div class="header-container">
        <div class="brand-text">ℒ - 𝒪</div>
        <div class="uthmani-text">
            بسم الله الرحمن الرحيم، الحمد لله الذي بنعمته تتم الصالحات.<br>
            <span class="pray-text">اللهم صل على سيدنا محمد وعلى آله وصحبه وسلم.</span>
        </div>
    </div>
""", unsafe_allow_html=True)

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except: return ""

departments = ["الفلسفة التطبيقية", "القانون (عام)", "القانون (خاص)", "الدراسات العربية", "الدراسات الإسلامية", "الدراسات الإنجليزية", "الدراسات الفرنسية", "الإقتصاد"]
semesters = ["S1", "S2", "S3", "S4", "S5", "S6"]

# --- الشريط الجانبي ---
with st.sidebar:
    img_data = get_image_base64("logo.png")
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="{img_data}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; max-width: 100%;">
            <div style="color: #bba14f; font-weight: bold; margin-top: 10px;">
                <div style="font-size: 1.2em;">L - O ❘ مكتبة الطلبة</div>
                <hr style="border-top: 2px solid #bba14f;">
                <div style="font-size: 0.9em; color: #333;">Bibliothèque des Étudiants</div>
                <div style="font-size: 0.8em; color: #666; margin-top: 5px;">~ ERRACHIDIA ~</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🔍 بحث خارجي (مكتبة نور)")
    noor_query = st.text_input("اسم الكتاب للبحث في نور:")
    if noor_query:
        st.link_button("ابحث في مكتبة نور ↗️", f"https://www.noor-book.com/books/search?query={noor_query}")
    
    st.markdown("---")
    
    if st.session_state.is_admin:
        st.subheader("إدارة المكتبة (خاص بالمدير)")
        st.success("الموقع متصل الآن بجداول Google Sheets.")
        st.link_button("📝 فتح جدول البيانات للتعديل", "https://docs.google.com/spreadsheets/d/1oBDLx7XpHFh9JHz-kUxak4PMaAVEBC9Os22TFg7CAIo/edit")
        if st.button("🔄 تحديث البيانات الآن"):
            st.cache_data.clear()
            st.rerun()

# --- التصميم الترحيبي ---
st.markdown("""
    <div class="welcome-box">
        <h2 style="margin: 0; font-family: 'Amiri', serif;">Azul imhdar n imteɣren ❘ مرحبا بطلبة الرشيدية</h2>
        <p style="margin: 15px 0 0; font-size: 1.2em; line-height: 1.6;">
            بوابة معرفية مفتوحة للجميع، تتضمن موارد ومصادر تعليمية متنوعة. تم تصميم هذا المحتوى خصيصاً لدعم طلبة الكلية متعددة التخصصات بالرشيدية في مسيرتهم الأكاديمية. لا تترددوا في الاستفادة منها.<br>
            <br><strong>_FPE Errachidia</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- تحميل البيانات وعرضها ---
try:
    df = load_data()
    
    filter_dept = st.selectbox("تصفح حسب الشعبة:", departments)
    filtered_df = df[df['الشعبة'] == filter_dept]

    for sem in semesters:
        with st.expander(f"المواد الخاصة بـ {sem}"):
            sem_books = filtered_df[filtered_df['الفصل'] == sem]
            
            if not sem_books.empty:
                cols = st.columns(4) 
                for i, (_, row) in enumerate(sem_books.iterrows()):
                    with cols[i % 4]:
                        title = str(row['اسم الكتاب'])
                        short_title = title[:15] + "..." if len(title) > 15 else title
                        st.write(f"📖 **{short_title}**")
                        
                        link = row['رابط التحميل']
                        if link != "":
                            st.link_button("تحميل / عرض", str(link), key=f"btn_{sem}_{i}")
                        else:
                            st.caption("(سيتم إضافته قريباً)")
            else:
                st.info("لا توجد ملفات في هذا الفصل حالياً.")

    st.markdown("---")
    st.subheader("✨ مكتبة المراجع والمصادر الإثرائية ✨")
    
    # تمت تنقية البيانات مسبقاً في دالة التحميل، الكود هنا أصبح بسيطاً وآمناً 100%
    extra_books = filtered_df[filtered_df['الفصل'] == "شامل"]
    
    if not extra_books.empty:
        for i, (_, eb) in enumerate(extra_books.iterrows()):
            col_text, col_btn = st.columns([4, 1])
            with col_text:
                st.write(f"📁 {eb['اسم الكتاب']}")
            with col_btn:
                link = eb['رابط التحميل']
                if link != "":
                    st.link_button("تحميل / عرض", str(link), key=f"extra_btn_{i}")
    else:
        st.info("لا توجد مراجع إضافية مضافة بعد في هذه الشعبة.")

except Exception as e:
    st.error(f"حدث خطأ في جلب البيانات: {e}")

# --- التذييل ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; font-family: sans-serif; color: #333; padding: 20px;">
        <div style="font-size: 1.1em; margin-bottom: 10px;">للمزيد من المساعدة والشرح أو تساؤل تواصل معي، لا تتردد في الضغط على الاسم</div>
        <div style="margin: 5px 0;">
            <a href="https://www.facebook.com/profile.php?id=100093495249631" style="font-weight: bold; color: #007bff; text-decoration: none; font-size: 1.2em;">LAHCEN OUKHOUAOU</a>
        </div>
        <div style="font-size: 35px; line-height: 1.5; background: linear-gradient(to bottom, blue, green, yellow); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ⵣ</div>
    </div>
""", unsafe_allow_html=True)
