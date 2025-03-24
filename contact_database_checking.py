import sqlite3
import streamlit as st

# Connect to the SQLite database
conn = sqlite3.connect("contact.db")
c = conn.cursor()

# Function to fetch and display contact data
def view_contact_data():
    st.title("📋 Submitted Contact Messages")

    # Fetch data from the database
    c.execute("SELECT * FROM contacts")
    data = c.fetchall()

    if data:
        for row in data:
            st.write(f"🆔 **ID:** {row[0]}")
            st.write(f"👤 **Name:** {row[1]}")
            st.write(f"📧 **Email:** {row[2]}")
            st.write(f"💬 **Message:** {row[3]}")
            st.write(f"📅 **Timestamp:** {row[4]}")
            st.markdown("---")  # Separator line
    else:
        st.info("📭 No messages found.")

# Run the function
if __name__ == "__main__":
    view_contact_data()
