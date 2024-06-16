import streamlit as st
import pandas as pd
import time
from PIL import Image 
import base64
import sqlite3
from streamlit.components.v1 import html
#網頁配置設定
st.set_page_config(
    page_title="World War II Museum",
    page_icon="random",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# 初始化資料庫
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        #使用側邊欄選擇框
        option = st.sidebar.selectbox(
    '',
    ['About Us','Contact Us','Top Up','Historical figures information','Product','History'])
        # 初始化資料庫
        conn = sqlite3.connect('credit_card.db')
        c = conn.cursor()

            # 創建表格
        c.execute('''
                CREATE TABLE IF NOT EXISTS credit_card (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_number TEXT UNIQUE,
                    expiration_day TEXT,
                    cvv TEXT,
                    is_deducted BOOLEAN DEFAULT FALSE
                )
            ''')

        conn.commit()
        if option == 'About Us':
         show_message = True
         st.header('Introduction')
         st.write("The War Museum was founded by Mr. Chen Yuhong in 1959 to showcase the history and impact of the war. The museum's collection includes weapons, uniforms, photographs, documents and other war-related artifacts to promote understanding of war and promote peace.")
         with st.expander("Founder"):
          st.write("Mr. Chen Yuhong is a retired soldier who served in World War II. He witnessed the brutality of war and determined to create a museum to show its cost. He hopes the museum will help people understand the history and impact of the war and promote peace.")
          image = Image.open('me.jpg')
          st.image (image, caption='', use_column_width=True)
         with st.expander("Museum History"):
          st.markdown("The War Museum was originally a small exhibition located in the home of Mr. Chen Yuhong. As the museum's collections and visitor numbers grew, it moved to a larger space. However, with the rise of the **Internet**, all the museum's collection information has been digitized, allowing more people who can't come here to view our historical introductions and products through the Internet. The museum's collections include **weapons. , uniforms, photographs, medals and other war-related artifacts**.")

        elif option == 'Contact Us':  
         show_message = True
         st.header('Contact Us')
         st.markdown('**We are available to answer your telephone call from Monday to Freiday during office hours.**')
         st.markdown('**Alternatively please contact us by email or post.**')
         st.markdown('*TEL:* ***00445435 15825***')
         st.markdown('*Email:* ***war@localhost8512.com***')
         st.divider()
         st.write('We reply to email enquiries within 3 working days or thereabouts.If your enquiry is particularly urgent and/or important,please kindly telephone (at caller-cost).')
         st.divider()
         col1, col2 = st.columns(2)
         with col1:
          st.markdown("**Registered Office**")
          st.write("Reception Ulric of England 35 Sandford Avenue Church Stretton SHROPSHIRE SY6 6BH")

         with col2:
          st.markdown("**Delivery Guidelines | Warehousing**")
          st.markdown("Our Registered Office serves as a temporary holding address for general mail and courier deliveries including consigned goods, unless otherwise agreed in writing. Goods delivered to our Registered Office are 'delivered for sale'. *If your shipment is important and/or valuable please contact us to arrange delivery.Our Warehouse provides storage for single items and collections at competitive rates. For a copy of our Storage Agreement and/or to discuss your storage requirements, please telephone.* goods are stored in our warehouse.")
          st.markdown('**Visiting us**')
          st.markdown('To arrange an appointment please telephone.Prospective visitors are kindly reminded we are a mail order company and do not have a physical shop.') 
          
        elif option == 'Top Up':  
         show_message = True
         def save_credit_card_info(card_number, expiration_day, cvv):
            c.execute("INSERT OR IGNORE INTO credit_card (card_number, expiration_day, cvv, is_deducted) VALUES (?,?,?,?)",
                    (card_number, expiration_day, cvv, False))  # 設定is_deducted為False
            conn.commit()



         def delete_all_data():
            # 刪除表格
            c.execute("DROP TABLE IF EXISTS credit_card")
            # 重新創建新表格
            c.execute('''
                CREATE TABLE IF NOT EXISTS credit_card (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_number TEXT UNIQUE,
                    expiration_day TEXT,
                    cvv TEXT,
                    is_deducted BOOLEAN DEFAULT FALSE 
                )
            ''')
            conn.commit()

         def display_credit_card_table():
            query = "SELECT * FROM credit_card"
            df = pd.read_sql_query(query, conn)
            st.write(' Your Credit Card Information ：')
            columns_to_display = ['id', 'card_number', 'expiration_day','is_deducted']
            df_display = df[columns_to_display]
            st.dataframe(df_display)

         def main():
            st.title("Top Up your points")

            # Credit Card Information
            card_number = st.text_input('Credit Card Number', max_chars=16)
            expiration_day = st.text_input('Expiration Day (MM/YY)', max_chars=7)
            cvv = st.text_input('CVV', type="password", max_chars=3)

            # Points Top-Up
            if 'total_points' not in st.session_state:
                st.session_state.total_points = 0
            top_up_amount = st.number_input('Enter the Top-up amount (Top up amount must less than 10000)', value=0)

            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                # Submit Button
                if st.button('Top up'):
                    with st.spinner('Recharge is being processed...'):
                     time.sleep(1.5)                    
                    # 檢查輸入的金額是否有效       
                    should_update_total_points = True
                    if top_up_amount >= 0 and top_up_amount < 10000 and card_number!= '' and expiration_day!= '' and cvv!= '' and len(card_number) == 16 and  len(expiration_day) == 7 and len(cvv) == 3 :
                        # 將目前輸入的金額加到總金額上 
                        st.session_state.total_points += top_up_amount
                        if st.session_state.total_points > 10000:
                            st.session_state.total_points = 10000
                            st.write(f"You have a balance of {st.session_state.total_points} points.")
                            st.info('Top-up amount exceeds the limit of 10000 points.')
                            should_update_total_points = False
                    elif top_up_amount >= 0 and top_up_amount < 10000 or card_number == '' or expiration_day == '' or cvv == '':
                        should_update_total_points = False
                    else:
                        st.write(f"You have a balance of {st.session_state.total_points} points.")
                        st.error('Recharge processed failed. Please enter a number within 10000')
                    
                    if should_update_total_points:
                        st.write(f"You have a balance of {st.session_state.total_points} points.")
                    else:
                        st.write(f"You have a balance of {st.session_state.total_points} points.")  # 保持總額不變

                    if card_number == '' and expiration_day == '' and cvv == '' and top_up_amount == 0:
                        st.warning('Please fill in the correct information.')                      
                    elif card_number == '' or len(card_number) < 16:
                        st.warning('Please fill in the correct Credit card number information.')
                    elif expiration_day == '' or len(expiration_day) < 7:
                        st.warning('Please fill in the correct Expiration day information.')
                    elif cvv == '' or len(cvv) < 3:
                        st.warning('Please fill in the correct CVV information.')
                    elif top_up_amount == 0:
                        st.warning('Please enter the amount you want to recharge.')
                    elif top_up_amount < 10000:
                        save_credit_card_info(card_number, expiration_day, cvv)
                        st.success('The recharge was successfully processed. Your credit card information has been saved.')

            with col2:
                # Delete All Data Button
                if st.button('Delete your credit card information'):
                    #清空儲值用的點數
                    st.session_state.total_points = 0
                    # 檢查表是否為空
                    check_empty_table = "SELECT COUNT(*) FROM credit_card"
                    result = pd.read_sql_query(check_empty_table, conn)
                    count = result.iloc[0, 0]  # 獲取記錄數
                    if count > 0:
                        delete_all_data()
                        st.success('All Credit Card deleted successfully.')
                    else:
                        st.info('You have not entered any credit card information.')

            # 顯示信用卡信息表格，只有在用戶點擊“Top Up”後才顯示
            if st.session_state.get('top_up_clicked', False):
                display_credit_card_table()

            # 更新 session_state 以反應用戶點擊“Top Up”按钮的事實
            st.session_state.top_up_clicked = True

         if __name__ == "__main__":
            main()

        elif option == 'Historical figures information':
         st.header('Historical figures information')
         st.subheader('Here is an introduction to famous historical figures from different countries. You can click the button according to the person you want to know about for a deeper understanding.')
         def open_url_in_new_tab(url):
          script = f"""
            <script type="text/javascript">
                window.open('{url}', '_blank').focus();
            </script>
        """
          html(script)

         tab1, tab2, tab3 = st.tabs(["Nazi Germany", "Empire of Japan", "Soviet Union"])
         with tab1:
          col1, _, col3 = st.columns(3)       
          with col1:    
           image = Image.open('Adolf Hitler.jpg')
           st.image (image, caption='阿道夫·希特勒(第三帝國元首兼納粹黨黨魁)', use_column_width=True)
           if st.button('Adolf Hitler'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E9%98%BF%E9%81%93%E5%A4%AB%C2%B7%E5%B8%8C%E7%89%B9%E5%8B%92')

           image = Image.open('hermann goring.jpg')
           st.image (image, caption='赫爾曼·威廉·戈林(帝國元帥兼空軍總司令)', use_column_width=True)
           if st.button('Hermann Göring'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E8%B5%AB%E5%B0%94%E6%9B%BC%C2%B7%E6%88%88%E6%9E%97')

           image = Image.open('heinrich himmler.jpg')
           st.image (image, caption='海因里希·盧伊特波爾德·希姆萊(親衛隊全國領袖兼內政部部長兼警察總長)', use_column_width=True)
           if st.button('Heinrich Himmler'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E6%B5%B7%E5%9B%A0%E9%87%8C%E5%B8%8C%C2%B7%E5%B8%8C%E5%A7%86%E8%8E%B1')

          with col3:
           image = Image.open('joseph gobbels.jpg')
           st.image (image, caption='保羅·約瑟夫·戈培爾(第三帝國總理兼國民教育與宣傳部部長)', use_column_width=True)
           if st.button('Joseph Goebbels'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E7%B4%84%E7%91%9F%E5%A4%AB%C2%B7%E6%88%88%E5%9F%B9%E7%88%BE')

           image = Image.open('reinhard heydrich.jpg')
           st.image (image, caption='萊因哈德·崔斯坦·歐根·海德里希(帝國安全部部長兼蓋世太保（秘密警察）首長兼親衛隊上級集團領袖兼警察上將)', use_column_width=True)
           if st.button('Reinhard Heydrich'):
            open_url_in_new_tab('https://zh.wikipedia.org/wiki/%E8%90%8A%E5%9B%A0%E5%93%88%E5%BE%B7%C2%B7%E6%B5%B7%E5%BE%B7%E9%87%8C%E5%B8%8C')

           image = Image.open('ribbentrop.jpg')
           st.image (image, caption='烏爾里希·弗里德里希·威廉·約阿希姆·馮·里賓特洛甫(外交部長)', use_column_width=True)
           if st.button('Joachim von Ribbentrop'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E7%BA%A6%E9%98%BF%E5%B8%8C%E5%A7%86%C2%B7%E5%86%AF%C2%B7%E9%87%8C%E5%AE%BE%E7%89%B9%E6%B4%9B%E7%94%AB')
        
         with tab2:
          col1, _, col3 = st.columns(3)           
          with col1:    
           image = Image.open('TENNO.jpg')
           st.image (image, caption='昭和天皇(天皇兼大日本帝國大元帥)', use_column_width=True)
           if st.button('しょうわてんのう'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E6%98%AD%E5%92%8C%E5%A4%A9%E7%9A%87')

           image = Image.open('TOJO.jpg')
           st.image (image, caption='東條英機(內閣總理大臣兼大日本帝國陸軍大將)', use_column_width=True)
           if st.button('とうじょう ひでき'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E4%B8%9C%E6%9D%A1%E8%8B%B1%E6%9C%BA')


          with col3:
           image = Image.open('YAMAMOTO.jpg')
           st.image (image, caption='山本五十六(海軍聯合艦隊司令長官兼海軍元帥)', use_column_width=True)
           if st.button('やまもと いそろく'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E5%B1%B1%E6%9C%AC%E4%BA%94%E5%8D%81%E5%85%AD')

           image = Image.open('YAMASHITA.jpg')
           st.image (image, caption='山下奉文(關東防衛軍司令官兼陸軍大將)', use_column_width=True)
           if st.button('やました ともゆき'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E5%B1%B1%E4%B8%8B%E5%A5%89%E6%96%87')

         with tab3:
          col1, _, col3 = st.columns(3)       
          with col1:    
           image = Image.open('FLADIMIR LENIN.jpg')
           st.image (image, caption='弗拉迪米爾·伊里奇·烏里揚諾夫(布爾什維克黨創始人兼蘇聯人民委員會主席)', use_column_width=True)
           if st.button('Влади́мир Улья́нов'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E5%BC%97%E6%8B%89%E5%9F%BA%E7%B1%B3%E5%B0%94%C2%B7%E5%88%97%E5%AE%81')

           image = Image.open('STALIN.jpg')
           st.image (image, caption='約瑟夫·維薩里奧諾維奇·史達林(蘇聯共產黨中央委員會總書記兼蘇聯最高領導人)', use_column_width=True)
           if st.button('Ио́сиф Ста́лин'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E7%BA%A6%E7%91%9F%E5%A4%AB%C2%B7%E6%96%AF%E5%A4%A7%E6%9E%97')

           image = Image.open('ZHUKOV.jpg')
           st.image (image, caption='喬治·康斯坦丁諾維奇·朱可夫(蘇聯元帥)', use_column_width=True)
           if st.button('Гео́ргий Жу́ков'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E6%A0%BC%E5%A5%A5%E5%B0%94%E5%9F%BA%C2%B7%E6%9C%B1%E5%8F%AF%E5%A4%AB')

          with col3:
           image = Image.open('BREZHNEV.jpg')
           st.image (image, caption='列昂尼德·伊里奇·布里茲涅夫(蘇聯最高蘇維埃主席團主席兼蘇聯共產黨中央委員會總書記)', use_column_width=True)
           if st.button('Леони́д Бре́жнев'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E5%88%97%E6%98%82%E5%B0%BC%E5%BE%B7%C2%B7%E5%8B%83%E5%88%97%E6%97%A5%E6%B6%85%E5%A4%AB')

           image = Image.open('KALASHINIKOV.jpg')
           st.image (image, caption='米哈伊爾·季莫費耶維奇·卡拉希尼柯夫(蘇聯中將兼AK47創始人)', use_column_width=True)
           if st.button('Михаил Калашников'):
            open_url_in_new_tab('https://zh.wikipedia.org/zh-tw/%E7%B1%B3%E5%93%88%E4%BC%8A%E5%B0%94%C2%B7%E5%8D%A1%E6%8B%89%E4%BB%80%E5%B0%BC%E7%A7%91%E5%A4%AB')


        elif option == 'Product':    
         show_message = True
         st.header('Products')
         tab1, tab2, tab3 = st.tabs(["Nazi Germany", "Empire of Japan", "Soviet Union"])
         with tab1:
          col1, _, col3 = st.columns(3)       
          with col1:
           if 'show_image1' not in st.session_state:
            st.session_state['show_image1'] = False        
           if st.button('Eisernes Kreuz Klasse II'):
            st.session_state['show_image1'] = not st.session_state['show_image1']  
           if st.session_state['show_image1']:
            st.image('2klass.png', caption='二级鐵十字勳章')
            st.write('獲得條件（通常）：在戰鬥中表現出一次非同尋常的勇敢行為，完成了自己的使命。二級鐵十字勳章用綬帶懸掛在胸口。')

           if 'show_image2' not in st.session_state:
            st.session_state['show_image2'] = False
           if st.button('Ritterkreuz des Eisernen Kreuzes'):
            st.session_state['show_image2'] = not st.session_state['show_image2']
           if st.session_state['show_image2']:
            st.image('Ritterkreuz.png', caption='騎士鐵十字勳章')
            st.write("獲得條件（通常）：被授予過一級鐵十字勳章或EK1的1939式裝飾品，並且繼續在戰鬥中表現出非同尋常的勇敢行為，完成了自己的使命。除上述條件外A.海軍潛艇部隊擊沉100,000噸位；B.空軍獲得20個勝利點（擊落單引擎敵機1點，雙引擎2點，四引擎3點。夜間任務點數雙倍）都可獲得騎士鐵十字勳章。配置於領子間")       

           if 'show_image3' not in st.session_state:
            st.session_state['show_image3'] = False
           if st.button('Ritterkreuz des Eisernen Kreuzes mit Eichenlaub und Schwertern'):         
            st.session_state['show_image3'] = not st.session_state['show_image3']
           if st.session_state['show_image3']:
            st.image('oak leaves sword.png', caption='橡葉帶劍騎士鐵十字勳章')
            st.write('獲得條件（通常）：被授予過橡葉騎士鐵十字勳章，並且繼續在戰鬥中表現出非同尋常的勇敢行為，完成了自己的使命。除上述條件外海軍潛艇部隊及空軍繼續勇敢完成任務，且不斷增長者都有機會獲得橡葉帶劍騎士鐵十字勳章（無固定標準）。')   

           if 'show_image4' not in st.session_state:
            st.session_state['show_image4'] = False
           if st.button('Ritterkreuz mit Goldenem Eichenlaub, Schwertern und Brillianten'):
            st.session_state['show_image4'] = not st.session_state['show_image4']
           if st.session_state['show_image4']:
            st.image('oak leaves sword diamond gold.png', caption='鑽石金橡葉金帶劍騎士鐵十字勳章')
            st.write('僅漢斯·魯德爾所擁有')   
 
          with col3:
           if 'show_image5' not in st.session_state:
            st.session_state['show_image5'] = False
           if st.button('Eisernes Kreuz Klasse I'):
            st.session_state['show_image5'] = not st.session_state['show_image5']
           if st.session_state['show_image5']:
            st.image('1st iron cross.png', caption='一级鐵十字勳章')
            st.write("被授予過二級鐵十字獎章或1939式二級鐵十字裝飾品，並在戰鬥中三到五次地表現出非同尋常的勇敢行為，完成了自己的使命。除上述條件外，海軍潛艇部隊擊沉50,000噸位；空軍獲得5個勝利點（擊落單引擎敵機1點，雙引擎2點，四引擎3點。夜間任務點數雙倍）都可獲得一級鐵十字勳章。")

           if 'show_image6' not in st.session_state:
            st.session_state['show_image6'] = False
           if st.button('Ritterkreuz des Eisernen Kreuzes mit Eichenlaub'):
            st.session_state['show_image6'] = not st.session_state['show_image6']
           if st.session_state['show_image6']:
            st.image('oak leaves.png', caption='橡葉騎士鐵十字勳章')
            st.write("獲得條件（通常）：被授予過騎士鐵十字勳章，並且繼續在戰鬥中表現出非同尋常的勇敢行為，完成了自己的使命。除上述條件外海軍潛艇部隊及空軍繼續勇敢完成任務，且不斷增長者都有機會獲得橡葉騎士鐵十字勳章（無固定標準）。")

           if 'show_image7' not in st.session_state:
            st.session_state['show_image7'] = False
           if st.button('Ritterkreuz mit Eichenlaub, Schwertern und Brillianten'):
            st.session_state['show_image7'] = not st.session_state['show_image7']
           if st.session_state['show_image7']:
            st.image('oak leaves sword diamond.png', caption='鑽石橡葉帶劍騎士鐵十字勳章')
            st.write("獲得條件（通常）：被授予過騎士鐵十字勳章，並且繼續在戰鬥中表現出非同尋常的勇敢行為，完成了自己的使命。除上述條件外海軍潛艇部隊及空軍繼續勇敢完成任務，且不斷增長者都有機會獲得橡葉騎士鐵十字勳章（無固定標準）。")

           if 'show_image8' not in st.session_state:
            st.session_state['show_image8'] = False
           if st.button('Großkreuz des Eisernen Kreuzes'):
            st.session_state['show_image8'] = not st.session_state['show_image8']
           if st.session_state['show_image8']:
            st.image('big iron.png', caption='大十字勛章')
            st.write("大十字勳章並不是用來獎勵英勇的。它是專門獎勵能夠作出「影響戰爭動向最傑出決策」的參謀軍官們。")
          st.divider()
          
         with tab2:
          col1, _, col3 = st.columns(3)
       
          with col1:
           if 'show_image9' not in st.session_state:
            st.session_state['show_image9'] = False
           if st.button('支那事変軍事記念メダル'):
            st.session_state['show_image9'] = not st.session_state['show_image9']
           if st.session_state['show_image9']:
            st.image('支那事變從軍紀念章.jpg', caption='支那事變從軍紀念章')
            st.write('授予1937年參加中國事變的日本軍人。')      

           if 'show_image10' not in st.session_state:
            st.session_state['show_image10'] = False
           if st.button('重傷メダル'):
            st.session_state['show_image10'] = not st.session_state['show_image10']
           if st.session_state['show_image10']:
            st.image('傷夷紀章.png', caption='傷夷紀章')
            st.write('授予於戰爭中受重傷的日本軍人。')         
          with col3:
           if 'show_image11' not in st.session_state:
            st.session_state['show_image11'] = False
           if st.button('大東亜戦争従軍記念勲章'):
            st.session_state['show_image11'] = not st.session_state['show_image11']
           if st.session_state['show_image11']:
            st.image('大東亞戰爭從軍紀念章.jpg', caption='大東亞戰爭從軍紀念章')
            st.write('授予參加與美國對抗的太平洋戰爭的日本軍人。')                
         with tab3:
          col1, _, col3 = st.columns(3)

          with col1:
           if 'show_image12' not in st.session_state:
            st.session_state['show_image12'] = False
           if st.button('Герой Советского Союза'):
            st.session_state['show_image12'] = not st.session_state['show_image12']
           if st.session_state['show_image12']:
            st.image('soviet hero.png', caption='蘇聯英雄(金星勳章)')
            st.write('是蘇聯勛賞制度中的最高榮譽，授予在為蘇聯國家和社會服務中作出英雄壯舉的個人或集體。蘇聯英雄一般授予軍人。')

           if 'show_image13' not in st.session_state:
            st.session_state['show_image13'] = False
           if st.button('Герой Социалистического Труда'):
            st.session_state['show_image13'] = not st.session_state['show_image13']
           if st.session_state['show_image13']:
            st.image('soviet labor hero.jpg', caption='社會主義勞動英雄')
            st.write("在經濟和文化領域作出重大貢獻者授予的最高榮譽。「社會主義勞動英雄」稱號只授予蘇聯公民。")       

           if 'show_image14' not in st.session_state:
            st.session_state['show_image14'] = False
           if st.button('Мать-героиня'):
            st.session_state['show_image14'] = not st.session_state['show_image14']
           if st.session_state['show_image14']:
            st.image('hero mother.png', caption='英雄母親')
            st.write('授予生育與扶養10名以上子女的蘇聯母親。')   

           if 'show_image15' not in st.session_state:
            st.session_state['show_image15'] = False
           if st.button('Орден Крaсного Знамени'):
            st.session_state['show_image15'] = not st.session_state['show_image15']
           if st.session_state['show_image15']:
            st.image('red flag.png', caption='紅旗勳章')
            st.write('授予軍事傑出表現者。在列寧勳章出現前，該勳章也是蘇聯唯一的軍事勳章。')   
 
           if 'show_image16' not in st.session_state:
            st.session_state['show_image16'] = False
           if st.button('Орден «Октябрьской Революции»'):
            st.session_state['show_image16'] = not st.session_state['show_image16']
           if st.session_state['show_image16']:
            st.image('october.png', caption='十月革命勳章')
            st.write('授予積極從事革命活動、為建成社會主義和建設共產主義、加強蘇聯的國防實力方面建立功勳，在同蘇維埃國家的敵人的戰鬥中表現特別勇敢，在發展國民經濟、科學文化方面取得重大成就、，以及為發展和加深蘇聯同其他國家人民之間的友好聯繫、為鞏固和平而積極工作的蘇聯公民、企業、機關、團體、勞動者群體、部隊和兵團，以及共和國、邊疆區、州和市。')   
                       
           if 'show_image17' not in st.session_state:
            st.session_state['show_image17'] = False
           if st.button('Орден Отечественной войны'):
            st.session_state['show_image17'] = not st.session_state['show_image17']
           if st.session_state['show_image17']:
            st.image('patriotic.jpg', caption='衛國戰爭勳章')
            st.write('授予所有在偉大衛國戰爭中做出英勇表現的蘇軍官兵、游擊隊、安全部隊成員。在1985年慶祝衛國戰爭40週年時，此章被頒授給所有在該戰爭存活下來的老兵，授予級別可能為一級或二級。')   

          with col3:
           if 'show_image18' not in st.session_state:
            st.session_state['show_image18'] = False
           if st.button('Орден Трудового Красного Знамени'):
            st.session_state['show_image18'] = not st.session_state['show_image18']
           if st.session_state['show_image18']:
            st.image('labor red flag.png', caption='勞動紅旗勳章')
            st.write("授予在勞動方面有出色成就的民間人士，對應授予軍人的紅旗勳章。")

           if 'show_image19' not in st.session_state:
            st.session_state['show_image19'] = False
           if st.button('Орден Ленина'):
            st.session_state['show_image19'] = not st.session_state['show_image19']
           if st.session_state['show_image19']:
            st.image('lenin.jpg', caption='列寧勳章')
            st.write("授給軍人或民間人士，同時也是後者所能獲得的最高級別勳章，授予條件為下列三者其一：在保衛祖國的戰鬥中表現非凡、鞏固國家和平或對社會有卓越勞動成就。")

           if 'show_image20' not in st.session_state:
            st.session_state['show_image20'] = False
           if st.button('Орден Красной Звезды'):
            st.session_state['show_image20'] = not st.session_state['show_image20']
           if st.session_state['show_image20']:
            st.image('red star.png', caption='紅星勳章')
            st.write("授予為在戰爭或和平時期、對蘇聯的國防事業有卓越貢獻的陸海軍成員。此章在長期服務獎勵創設前，也曾授給服務15年以上的蘇聯官兵。")

           if 'show_image21' not in st.session_state:
            st.session_state['show_image21'] = False
           if st.button('Орден Победа'):
            st.session_state['show_image21'] = not st.session_state['show_image21']
           if st.session_state['show_image21']:
            st.image('victory.jpg', caption='勝利勳章')
            st.write("授予順利完成一個或數個方面軍參加的大型戰役，而使戰略態勢發生了有利於蘇軍變化的蘇聯武裝力量最高級指揮人員。")

           if 'show_image22' not in st.session_state:
            st.session_state['show_image22'] = False
           if st.button('Юбилейная медаль «В ознаменование 100-летия со дня рождения Владимира Ильича Ленина»'):
            st.session_state['show_image22'] = not st.session_state['show_image22']
           if st.session_state['show_image22']:
            st.image('100 years Lenin.png', caption='紀念列寧誕辰一百週年獎章')
            st.write('授予在列寧紀念日活動準備過程中及在軍事、政治訓練工作中取得優異成績的工人、集體農莊莊員、國民經濟專家、國家機關和社會組織工作人員、科學和文化活動家、蘇聯武裝力量軍人、內務部機關和部隊官兵、國家安全委員會人員，以及為建立蘇維埃政權積極參加戰鬥或保衛國家貢獻突出的人、國際共產主義運動和工人運動活動家。分為忘我勞動版、軍人英勇版以及無字版（授予外國人）。')   
          st.divider()

        elif option == 'History':
         option1 = st.sidebar.selectbox(
    'Which Countrys history do you want to konw？',
    ['Nazi Germany','Empire of Japan','Soviet Union'])

         if option1 == 'Nazi Germany':
          show_message = True
          st.header('Nationalsozialistische Deutschland')
          st.info('Welcome to Nazi Germany page')
          time.sleep(0.5)
          image = Image.open('nazi party.jpg')
          st.image (image, caption='Nazi Germany', use_column_width=True)
   
          tab1, tab2, tab3 = st.tabs(["Pre War", "WWII", "End War"])

          with tab1:
           st.markdown('**_Pre_ War**')
           image = Image.open('wwi lose.jpg')
           st.image (image, caption='', use_column_width=True)
           st.image('1929 economic.jpg', caption='經濟大蕭條')
           image = Image.open('nazi rise.jpg')
           st.image (image, caption='', use_column_width=True)
       
           #gif檔案轉換及匯入
           file_ = open("Nazi rise.gif", "rb")
           contents = file_.read()
           # 將 GIF 檔案轉換為 base64 編碼
           data_url = base64.b64encode(contents).decode("utf-8")
           file_.close()
           # 在 Streamlit app 中顯示 GIF
           st.markdown(
           f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
           unsafe_allow_html=True,)
           st.markdown('納粹崛起')

          with tab2:
           st.markdown('**_WWII_**')
           image = Image.open('stage 1.jpg')
           st.image (image, caption='', use_column_width=True)
      
           #gif檔案轉換及匯入
           file_ = open("1939wwii.gif", "rb")
           contents = file_.read()
           # 將 GIF 檔案轉換為 base64 編碼
           data_url = base64.b64encode(contents).decode("utf-8")
           file_.close()
           # 在 Streamlit app 中顯示 GIF
           st.markdown(
           f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
           unsafe_allow_html=True,)
           st.markdown('瓜分波蘭')

           image = Image.open('stage 2.jpg')
           st.image (image, caption='', use_column_width=True)
           #gif檔案轉換及匯入
           file_ = open("Nazi expand.gif", "rb")
           contents = file_.read()
           # 將 GIF 檔案轉換為 base64 編碼
           data_url = base64.b64encode(contents).decode("utf-8")
           file_.close()
           # 在 Streamlit app 中顯示 GIF
           st.markdown(
           f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
           unsafe_allow_html=True,)
           st.markdown('入侵蘇聯')

          with tab3:
           option2 = st.selectbox(
            'You can pay or choose to recharge',
            ('Preview Version','Full Version', 'Top up')
           )
           if option2 == 'Preview Version':
              st.markdown('**_End_ War**')
              image = Image.open('end war.jpg')
              st.image (image, caption='', use_column_width=True)
              video_file1 = open('end war(pre view).mp4', 'rb')
              video_bytes = video_file1.read()
              st.video(video_bytes)
              st.info("If you want to watch the full version, Please pay 250 points to experience the full version.")


           if option2 == ('Full Version'):
              if 'change_page2'not in st.session_state:#(當st.button("Pay for it")消失後，若有從其他頁面切換回此頁面，則回來到這段程式，這段是讓第二次點擊的程式關閉以及按鈕的程式關閉。)
                st.session_state['change_page2']=False       
              if st.session_state['change_page2']:
                st.markdown(f"You have blance of :blue[{st.session_state.total_points}] point.")
                video_file = open('end war.mp4', 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                st.text('The destruction of the Third Reich')  
                st.session_state['change_page1']=False
         
          
              if 'change_page1'not in st.session_state:#(點擊st.button("Pay for it")第二次會來到這段程式，主要是為了能夠讓按鈕消失然後影片持續存在，同時也為讓st.session_state['change_page2']等於True。)
                st.session_state['change_page1']=False       
              if st.session_state['change_page1']:
                st.info('You have paid successfully.')  
                st.markdown(f"You have blance of :blue[{st.session_state.total_points}] point.")
                video_file = open('end war.mp4', 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                st.text('The destruction of the Third Reich')
                st.session_state['change_page2'] = not st.session_state['change_page2']
                st.session_state['change_page3']=False 
                
              if 'change_page3'not in st.session_state:
                st.session_state['change_page3']=True
              if st.session_state['change_page3']:      
               if st.button("Pay for it"):
                 if 'video_played' not in st.session_state:# 新增的步驟：檢查影片是否已經被播放 
                        st.session_state.video_played = False  # 初始化視頻播放狀態為未播放                  
                    # Points Top-Up 先初始化防止被衝塔(session_state一開始是空值，所以直接點Pay for it按鈕，會造成系統崩潰，所以先初始化 st.session_state.total_points = 0)
                 if 'total_points' not in st.session_state:
                        st.session_state.total_points = 0
                 st.session_state.total_points_save = st.session_state.total_points  #是先存放金額，已被後續st.session_state.total_points < 0時使用。

                 if 'first_time_deduct' not in st.session_state:#檢查用戶是否嘗試首次扣除點數
                        st.session_state.first_time_deduct = True            
                 if st.session_state.first_time_deduct:
                  st.session_state.total_points -= 250
                  st.session_state.first_time_deduct = False# 關閉此段程式，防止二次扣除

                 if 'second_time_deduct' not in st.session_state:#檢查用戶是否嘗試首次扣除點數
                        st.session_state.second_time_deduct =  False            
                 if st.session_state.second_time_deduct and st.session_state.total_points>=250:
                  st.session_state.total_points -= 250
                  st.session_state.second_time_deduct = False# 關閉此段程式，防止二次扣除

                 if st.session_state.total_points < 0:
                            if st.session_state.total_points_save == 0:  #這段是如果一開始就直接點Pay for it按鈕的話，就顯示沒有輸入信用卡，並顯示餘額為零。
                                with st.spinner('Paymemt is being processed...'):
                                 time.sleep(1.5)                                
                                st.warning("You didn't fill in your credit card on the Top up page. Please do not click the button again ! ")
                                st.info('If you want to recharge, be sure to recharge more than 250 points')#寫這個其實是因為如果點數不足夠，然後回儲值頁面時，儲值的點數加起來沒超過250(設定好的點數)點數的話，再切回這個畫面->[Full Version]，點擊按鈕時會造成點數不足以付款，卻能夠成功付款的BUG。
                                st.session_state.total_points = st.session_state.total_points_save   
                                st.markdown(f"You have blance of :blue[{st.session_state.total_points}] point.")
                                st.session_state.second_time_deduct = True
                            else:                                        #這段是一開始有輸入卡號儲值成功，且儲值金額小於物件所需支付金額時，就會顯示餘額不足，並顯示原先儲值金額。
                                with st.spinner('Paymemt is being processed...'):
                                 time.sleep(1.5)                               
                                st.warning("You don't have enough point to pay. Please do not click the button again !")
                                st.info('If you want to return to the Top up page, be sure not to click the delete credit card button, otherwise the points will be reset.')#寫這個警語其實是因為如果有餘額但不夠付款時，想回儲值頁面儲值，卻不小心按到刪除信用卡，則回來此頁面後，點選付款按鈕就會造成能夠付款的BUG。
                                st.session_state.total_points = st.session_state.total_points_save
                                st.markdown(f"You have blance of :blue[{st.session_state.total_points}] point.")
                                st.session_state.second_time_deduct = True
                                
                 elif st.session_state.total_points == 0 or st.session_state.total_points > 0: #(按鈕點擊一次)這段是儲值金額大於支付所需金額，且扣除所需金額後餘額剩餘0或大於0，就會顯示成功儲值，並顯示付款後的金額，最後顯示購買後的物件。
                            if not st.session_state.video_played:
                                with st.spinner('Paymemt is being processed...'):
                                 time.sleep(1.5)
                                st.session_state['change_page1'] = not st.session_state['change_page1']
                                st.success('Payment Successful.')              
                                st.markdown(f"You have blance of :blue[{st.session_state.total_points}] point.")
                                video_file = open('end war.mp4', 'rb')
                                video_bytes = video_file.read()
                                st.video(video_bytes)
                                st.text('The destruction of the Third Reich')
                                st.session_state.video_played = True
                                st.session_state['check if paid']=True
           elif option2 == ('Top up'):
             st.write('If you wnat to recharge,You need to go to the Top up page' )

         elif option1 == 'Empire of Japan':
           show_message = True
           st.header('だいにっぽんていこく')
           st.info('Welcome to Empire of Japan page')
           time.sleep(0.5)
           image = Image.open('japan longest day.jpg')
           st.image (image, caption='日本のいちばん長い日', use_column_width=True)
           col4, col5, col6 = st.columns(3)

           with col4:
            if st.button('1937-1941'):
             st.divider()
             st.header("支那事変")
             st.write("1937年7月7日，日軍在盧溝橋發動攻擊，史稱「七七事變」。中國國民政府軍隊奮起抵抗，抗日戰爭全面爆發。日軍企圖速戰速決，以優勢兵力向華北推進。國民政府軍隊浴血奮戰，在上海、南京等地進行頑強抵抗，但最終未能阻止日軍的進攻。")
             image = Image.open('sino-japan war.jpg')
             st.image (image, caption='侵華戰爭', use_column_width=True)
    
           with col5:
            if st.button('1941-1945'):
             st.divider()
             st.header("→大東亜戦争")
             st.write("1941年12月7日，日本偷襲珍珠港，太平洋戰爭爆發。日軍迅速佔領了東南亞和太平洋的大部分地區，形成了從日本到印度尼西亞的「大東亞共榮圈」。")
             #gif檔案轉換及匯入
             file_ = open("japan territory.gif", "rb")
             contents = file_.read()
             # 將 GIF 檔案轉換為 base64 編碼
             data_url = base64.b64encode(contents).decode("utf-8")
             file_.close()
             # 在 Streamlit app 中顯示 GIF
             st.markdown(
             f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
             unsafe_allow_html=True,)

           with col6:
             if st.button('1945/8/15'):
              st.divider()
              st.header("→終戦日")
              st.write("到了戰爭末期廣島以及長崎分別接連被投下原子彈造成大量死傷，而蘇聯也隨即參戰。")

              #gif檔案轉換及匯入
              file_ = open("nuclear bomb.gif", "rb")
              contents = file_.read()
              # 將 GIF 檔案轉換為 base64 編碼
              data_url = base64.b64encode(contents).decode("utf-8")
              file_.close()
              # 在 Streamlit app 中顯示 GIF
              st.markdown(
              f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
              unsafe_allow_html=True,)
              st.write("於上述情形迫使日本最終於1945年8月15日停止戰爭，並投降於盟軍中國戰區。")
              image = Image.open('japan surrender.jpg')
              st.image (image, caption='受降儀式', use_column_width=True)
           st.divider()
           if st.button('Play'):
            if 'check if paid'not in st.session_state:
               st.session_state['check if paid']=False    
            if st.session_state['check if paid']:
                video_file = open('戦後70年。日本人として知っておくべき歴史の真実。『日本のいちばん長い日』特別映像.mp4', 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                st.text('The Longest Day in Japan')
            else:
              video_file = open('戦後70年。日本人として知っておくべき歴史の真実。『日本のいちばん長い日』特別映像(preview).mp4', 'rb')
              video_bytes = video_file.read()
              st.video(video_bytes)
              st.text('The Longest Day in Japan')              
              st.info('If you want to watch the full version, please go to the Nazi Germany page to purchase the permission to watch the full version.')  
                    
         elif option1 == 'Soviet Union':
            show_message = True
            st.header('Союз Советских Социалистических Республик')
            st.info('Welcome to Soviet Union page')
            time.sleep(0.5)
            image = Image.open('duma.png')
            st.image (image, caption='Soviet Union', use_column_width=True)
            values = st.slider('Choose a Range: {1917-1945},{1945-1980}, {1980-1991}', 1917, 1991, (1917, 1945))
            st.divider()

            if values ==(1917,1945):
             st.subheader('October Revolution')
             with st.expander("people's war"):
              st.write("1917年,俄國爆發了十月革命,推翻了沙皇統治。1922年,蘇聯正式成立。在列寧和斯大林的領導下,蘇聯建立了社會主義制度,並取得了快速的經濟發展。")
              image = Image.open('october revolution.jpg')
              st.image (image, caption='十月革命', use_column_width=True)
       
             st.subheader('Patriotic War')
             with st.expander("The moment of national survival"):
              st.write("納粹德國於1941年,德國入侵蘇聯,蘇聯衛國戰爭爆發,最終以犧牲極大傷亡,成功抵擋德軍攻克莫斯科。")
              #gif檔案轉換及匯入
              file_ = open("NAZI INVANSION.gif", "rb")
              contents = file_.read()
              # 將 GIF 檔案轉換為 base64 編碼
              data_url = base64.b64encode(contents).decode("utf-8")
              file_.close()
              # 在 Streamlit app 中顯示 GIF
              st.markdown(
              f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
              unsafe_allow_html=True,)
              st.write("後期蘇軍發起反攻的號角,並在蘇聯人民的英勇抗戰下。一步一步往納粹德國的心腹「柏林」前進。")
              #gif檔案轉換及匯入
              file_ = open("soviet invasion.gif", "rb")
              contents = file_.read()
              # 將 GIF 檔案轉換為 base64 編碼
              data_url = base64.b64encode(contents).decode("utf-8")
              file_.close()
              # 在 Streamlit app 中顯示 GIF
              st.markdown(
              f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
              unsafe_allow_html=True,)
              st.write("最終德軍最終被擊敗。而首都柏林也被蘇聯成功奪下，至此蘇聯在第二次世界大戰中取得了巨大的勝利,成為世界強國之一。")
              image = Image.open('soviet flag.jpeg')
              st.image (image, caption='攻克柏林', use_column_width=True)
       
             if st.button('Play'):
              if 'check if paid'not in st.session_state:
                st.session_state['check if paid']=False    
              if st.session_state['check if paid']:
                st.write("共產主義至此蔓延世界各地")
                video_file = open('soviet.mp4', 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                st.text('Союз Советских Социалистических Республик')
              else:
                st.write("共產主義至此蔓延世界各地")
                video_file = open('soviet(preview).mp4', 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                st.text('Союз Советских Социалистических Республик')
                st.info('If you want to watch the full version, please go to the Nazi Germany page to purchase the permission to watch the full version.')               

            if values ==(1945,1980):
             st.subheader('Cold War')
             with st.expander("New World Order"):
              st.write("二戰過後，蘇聯將共產主義更加散播至周圍國家使其成為衛星國並組成東方集團。")
              #gif檔案轉換及匯入
              file_ = open("soviet expand.gif", "rb")
              contents = file_.read()
              # 將 GIF 檔案轉換為 base64 編碼
              data_url = base64.b64encode(contents).decode("utf-8")
              file_.close()
              # 在 Streamlit app 中顯示 GIF
              st.markdown(
              f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
              unsafe_allow_html=True,)
 
              st.write("受到蘇聯影響的東歐國家，一個接著一個投向共產主義的懷抱。")
              image = Image.open('soviet territory.jpg')
              st.image (image, caption='共產主義蔓延', use_column_width=True)
       
              st.write("而中西歐各資本主義國家感受共產主義的威脅，紛紛於1949年4月4日組成以美國為首的資本主義集團(北約)，隨後東歐各國與中亞國家於1955年5月14日組成以蘇聯為首的共產主義聯盟(華約)。")
              #gif檔案轉換及匯入
              file_ = open("enlargement of NATO.gif", "rb")
              contents = file_.read()
              # 將 GIF 檔案轉換為 base64 編碼
              data_url = base64.b64encode(contents).decode("utf-8")
              file_.close()
              # 在 Streamlit app 中顯示 GIF
              st.markdown(
              f'<img src="data:image/gif;base64,{data_url}" alt="animated gif">',
              unsafe_allow_html=True,) 
              st.write("至此整個歐洲以鐵幕為界線分裂成東西兩大集團的勢力範圍互相對抗。")
              image = Image.open('iron curtain.jpg')
              st.image (image, caption='歐洲鐵幕', use_column_width=True)
              st.write("最終以冷戰的開端造就了整個世界的新秩序")
              image = Image.open('cold war.jpg')
              st.image (image, caption='世界新秩序', use_column_width=True)
        
            if values ==(1980,1991):
             with st.expander("Disintegration of the soviet union"):
              st.write("自1953年史達林逝世後，蘇聯貪汙腐敗的情形逐漸浮上檯面並且各屆領導人治理方針多採取史達林時期的經濟模式，導致蘇聯國力逐漸下滑，再加上各加盟國逐漸出現民主化的聲浪使得蘇聯政府派駐軍隊前往鎮壓。")  
              image = Image.open('berlin wall.jpg')
              st.image (image, caption='東歐民主化(1989年柏林圍牆倒塌)', use_column_width=True)
              st.write("然而在1991年政變的情況下，使得屹立70餘年的蘇聯最終走向解體的道路。")
              image = Image.open('coup.jpg')
              st.image (image, caption='時任俄羅斯聯邦總統葉爾欽位於莫斯科白宮發佈政變聲明', use_column_width=True)
      
              video_file = open('anthem soviet.mp4', 'rb')
              video_bytes = video_file.read()
              st.video(video_bytes)
        if st.sidebar.button("Log out"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.experimental_rerun()
    else:
        menu = ["登入", "註冊"]
        choice = st.sidebar.selectbox("選擇操作", menu)

        if choice == "登入":
            login()
        elif choice == "註冊":
            signup()
def has_been_deducted(card_number):
    c.execute("SELECT is_deducted FROM credit_card WHERE card_number =?", (card_number,))
    result = c.fetchone()
    return result is not None and result[0]  # 如果找到了紀錄且is_deducted為True，則返回True

def login():
    st.title("Please log in or register")
    st.divider()    
    username = st.text_input("account")
    password = st.text_input("password", type="password")

    if st.button("Lon in"):
        user = validate_login(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            with st.spinner('Wait for it...'):
             time.sleep(1.5)
             st.success("Log in successfully！")
             st.experimental_rerun()

        else:
            with st.spinner('Wait for it...'):
             time.sleep(1.5)
             st.error("Wrong account or password!")

def signup():
    st.subheader("Register new account")
    
    new_username = st.text_input("New account")
    new_password = st.text_input("New password", type="password")

    if st.button("Register"):
        if not validate_signup(new_username):
            create_user(new_username, new_password)
            st.success("Registration successfully，please log in！")
        else:
            st.error("Account exists,please use another account.")


def validate_login(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone()

def validate_signup(username):
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    return c.fetchone()

def create_user(username, password):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

if __name__ == "__main__":
    main()