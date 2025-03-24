import streamlit as st  # Import Streamlit immediately after setting page config

# ✅ Set Page Configuration FIRST
st.set_page_config(
    page_title="Multimodal Deepfake Detector",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)



import time
from utils.auth import login_user, register_user, create_users_table
from pages.home import home_page
from pages.upload import upload_page
from pages.about import about_page
from pages.contact import contact_page
from pages.faq import faq_page  # Import FAQ Page

# ✅ Hide Sidebar Completely
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* ✅ Set Max Width for Better Layout */
    .main-container {
        max-width: 1100px;  /* Adjust width */
        margin: auto;  /* Center content */
    }

    /* ✅ Sticky Navigation Bar */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 15px;  /* Adjusted padding */
        background-color: #2D3250;
        border-radius: 8px;
        width: 100%;
        position: fixed;
        top: 0; 
        left: 0;
        z-index: 999;
    }

    .nav-left {
        display: flex;
        gap: 6px;
    }

    .nav-item {
        font-size: 14px;
        font-weight: normal;
        cursor: pointer;
        text-decoration: none;
        color: #ffffff;
        padding: 6px 10px;
        border-radius: 4px;
        transition: background 0.3s ease-in-out;
    }

    .nav-item:hover {
        text-decoration: underline;
    }

    .active-nav {
        font-weight: bold;
        border-bottom: 2px solid #ffffff;
        padding-bottom: 3px;
    }

    .logout-button {
        background-color: #E63946;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 14px;
        cursor: pointer;
        transition: background 0.3s ease-in-out;
    }

    .logout-button:hover {
        background-color: #C92A2A;
    }

    /* ✅ Adjust Content to Avoid Overlap */
    .block-container {
        padding-top: 60px !important;  
    }
    </style>
""", unsafe_allow_html=True)


# ✅ Initialize Session States
def initialize_session():
    session_defaults = {
        "menu": "Home",
        "logged_in": False,
        "show_login": False,
        "show_register": False
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session()


# ✅ Navigation Menu
def navbar():
    menu = ["Home", "About", "Contact", "Upload", "FAQ"]

    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    st.markdown('<div class="nav-left">', unsafe_allow_html=True)

    cols = st.columns(len(menu) + (1 if st.session_state["logged_in"] else 0))

    for i, item in enumerate(menu):
        if item == st.session_state["menu"]:
            cols[i].markdown(f'<span class="nav-item active-nav">{item}</span>', unsafe_allow_html=True)
        else:
            if cols[i].button(item, key=item):
                st.session_state["menu"] = item
                st.rerun()

    if st.session_state["logged_in"]:
        if cols[-1].button("Logout", key="logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["menu"] = "Home"
            st.session_state["show_login"] = False
            st.session_state["show_register"] = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ✅ Main Function
def main():
    navbar()

    # ✅ Center and Limit Content Width
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    if st.session_state["menu"] == "Home":
        home_page()
    elif st.session_state["menu"] == "About":
        about_page()
    elif st.session_state["menu"] == "Contact":
        contact_page()
    elif st.session_state["menu"] == "Upload":
        if st.session_state["logged_in"]:
            upload_page()
        else:
            st.warning("⚠️ Please log in to access this section.")
    elif st.session_state["menu"] == "FAQ":
        faq_page()

    st.markdown('</div>', unsafe_allow_html=True)  # ✅ End of centered container


# ✅ Run Application
if __name__ == "__main__":
    create_users_table()
    main()
