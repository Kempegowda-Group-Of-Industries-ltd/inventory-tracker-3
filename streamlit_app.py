from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd

import streamlit as st
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(page_title="Inventory Tracker", page_icon="📦", layout="wide")


import streamlit as st


import streamlit as st
import requests
from streamlit_lottie import st_lottie
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json
import streamlit as st
import requests
from streamlit_lottie import st_lottie




import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json





import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Inventory Animation
inventory_lottie = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_ydo1amjm.json")

# Theme Toggle (Light/Dark Mode)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

mode = st.sidebar.radio("🎨 Select Theme", ("Light", "Dark"))
st.session_state.dark_mode = mode == "Dark"

# Background and Text Theme
light_css = """
<style>
body {
    background: linear-gradient(to right, #f9f9f9, #e0eafc);
}
h1, h2, h3, p, label {
    color: #111 !important;
}
</style>
"""

dark_css = """
<style>
body {
    background: linear-gradient(to right, #232526, #414345);
}
h1, h2, h3, p, label {
    color: #eee !important;
}
</style>
"""

st.markdown(dark_css if st.session_state.dark_mode else light_css, unsafe_allow_html=True)

# Login function
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""

    if not st.session_state.authenticated:
        col1, col2 = st.columns([1, 2])
        with col1:
            st_lottie(inventory_lottie, height=250)
        with col2:
            st.markdown("<h2 style='text-align:center;'>🔐 Admin Login</h2>", unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                if submitted:
                    if username == "admin" and password == "Suhas@123":
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login successful! 🎉")
                    else:
                        st.error("Invalid username or password 🚫")
    return st.session_state.authenticated

# Login gate
if not login():
    st.stop()

# --- Main App Content ---
st.markdown(f"""
    <h1 style='text-align:center; animation: fadeIn 1.5s;'>📦 Inventory Tracker Dashboard</h1>
    <h4 style='text-align:center; margin-bottom:30px;'>Welcome <b>{st.session_state.username}</b>! Track and manage inventory efficiently.</h4>
""", unsafe_allow_html=True)

# Stylish card section
st.markdown("""
<style>
.card {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 15px;
    background-color: rgba(255,255,255,0.1);
    backdrop-filter: blur(5px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 40px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='card'><h3>➕ Add Item</h3><p>Enter and manage new inventory items.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'><h3>📊 View Stock</h3><p>See current stock levels and trends.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='card'><h3>🚨 Alerts</h3><p>Get alerts for low or critical stock.</p></div>", unsafe_allow_html=True)

# Optional logout
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", key="logout_button"):
    st.session_state.authenticated = False
   # st.experimental_rerun()  Rerun to show the login page

# Some logic or user interaction
if st.button("Rerun", key="rerun_button"):
    st.experimental_rerun()

# Optional: Add the logout button at the top or sidebar
#if st.sidebar.button("🚪 Logout", key="logout_sidebar"):
   # st.session_state.authenticated = False
   # st.experimental_rerun()
    
# Simulate an authentication state (use this as a flag to track login status)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Sidebar Logout Button
#st.sidebar.markdown("---")
#if st.sidebar.button("🚪 Logout", key="sidebar_logout_button"):
    # Set authentication to False
   # st.session_state.authenticated = False
    # Trigger rerun to redirect to login page
    #st.experimental_rerun()

# Login page logic
if not st.session_state.authenticated:
    # This is the login page (you can customize this as needed)
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Sample credentials check (you can modify this as per your requirements)
    if st.button("Login", key="login_button"):
        if username == "admin" and password == "password":  # Change to your credentials
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Please try again.")

# The main app page (accessible only if authenticated)
if st.session_state.authenticated:
    st.title("Welcome to the Admin Dashboard!")
    st.write("This is where your app content goes.")
    
# -----------------------------------------------------------------------------
# Declare some useful functions.


def connect_db():
    """Connects to the sqlite database."""

    DB_FILENAME = Path(__file__).parent / "inventory.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    """Initializes the inventory table with some data."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            price REAL,
            units_sold INTEGER,
            units_left INTEGER,
            cost_price REAL,
            reorder_point INTEGER,
            description TEXT
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO inventory
            (item_name, price, units_sold, units_left, cost_price, reorder_point, description)
        VALUES
            -- Beverages
            ('Bottled Water (500ml)', 1.50, 115, 15, 0.80, 16, 'Hydrating bottled water'),
            ('Soda (355ml)', 2.00, 93, 8, 1.20, 10, 'Carbonated soft drink'),
            ('Energy Drink (250ml)', 2.50, 12, 18, 1.50, 8, 'High-caffeine energy drink'),
            ('Coffee (hot, large)', 2.75, 11, 14, 1.80, 5, 'Freshly brewed hot coffee'),
            ('Juice (200ml)', 2.25, 11, 9, 1.30, 5, 'Fruit juice blend'),

            -- Snacks
            ('Potato Chips (small)', 2.00, 34, 16, 1.00, 10, 'Salted and crispy potato chips'),
            ('Candy Bar', 1.50, 6, 19, 0.80, 15, 'Chocolate and candy bar'),
            ('Granola Bar', 2.25, 3, 12, 1.30, 8, 'Healthy and nutritious granola bar'),
            ('Cookies (pack of 6)', 2.50, 8, 8, 1.50, 5, 'Soft and chewy cookies'),
            ('Fruit Snack Pack', 1.75, 5, 10, 1.00, 8, 'Assortment of dried fruits and nuts'),

            -- Personal Care
            ('Toothpaste', 3.50, 1, 9, 2.00, 5, 'Minty toothpaste for oral hygiene'),
            ('Hand Sanitizer (small)', 2.00, 2, 13, 1.20, 8, 'Small sanitizer bottle for on-the-go'),
            ('Pain Relievers (pack)', 5.00, 1, 5, 3.00, 3, 'Over-the-counter pain relief medication'),
            ('Bandages (box)', 3.00, 0, 10, 2.00, 5, 'Box of adhesive bandages for minor cuts'),
            ('Sunscreen (small)', 5.50, 6, 5, 3.50, 3, 'Small bottle of sunscreen for sun protection'),

            -- Household
            ('Batteries (AA, pack of 4)', 4.00, 1, 5, 2.50, 3, 'Pack of 4 AA batteries'),
            ('Light Bulbs (LED, 2-pack)', 6.00, 3, 3, 4.00, 2, 'Energy-efficient LED light bulbs'),
            ('Trash Bags (small, 10-pack)', 3.00, 5, 10, 2.00, 5, 'Small trash bags for everyday use'),
            ('Paper Towels (single roll)', 2.50, 3, 8, 1.50, 5, 'Single roll of paper towels'),
            ('Multi-Surface Cleaner', 4.50, 2, 5, 3.00, 3, 'All-purpose cleaning spray'),

            -- Others
            ('Lottery Tickets', 2.00, 17, 20, 1.50, 10, 'Assorted lottery tickets'),
            ('Newspaper', 1.50, 22, 20, 1.00, 5, 'Daily newspaper')
        """
    )
    conn.commit()


def load_data(conn):
    """Loads the inventory data from the database."""
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "id",
            "item_name",
            "price",
            "units_sold",
            "units_left",
            "cost_price",
            "reorder_point",
            "description",
        ],
    )

    return df


def update_data(conn, df, changes):
    """Updates the inventory data in the database."""
    cursor = conn.cursor()

    if changes["edited_rows"]:
        deltas = st.session_state.inventory_table["edited_rows"]
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            """
            UPDATE inventory
            SET
                item_name = :item_name,
                price = :price,
                units_sold = :units_sold,
                units_left = :units_left,
                cost_price = :cost_price,
                reorder_point = :reorder_point,
                description = :description
            WHERE id = :id
            """,
            rows,
        )

    if changes["added_rows"]:
        cursor.executemany(
            """
            INSERT INTO inventory
                (id, item_name, price, units_sold, units_left, cost_price, reorder_point, description)
            VALUES
                (:id, :item_name, :price, :units_sold, :units_left, :cost_price, :reorder_point, :description)
            """,
            (defaultdict(lambda: None, row) for row in changes["added_rows"]),
        )

    if changes["deleted_rows"]:
        cursor.executemany(
            "DELETE FROM inventory WHERE id = :id",
            ({"id": int(df.loc[i, "id"])} for i in changes["deleted_rows"]),
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
"""
# :shopping_bags: Inventory tracker

**Welcome to Alice's Corner Store's intentory tracker!**
This page reads and writes directly from/to our inventory database.
"""

st.info(
    """
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    """
)

# Connect to database and create table if needed
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast("Database initialized with some sample data.")

# Load data from database
df = load_data(conn)

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    column_config={
        # Show dollar sign before price columns.
        "price": st.column_config.NumberColumn(format="$%.2f"),
        "cost_price": st.column_config.NumberColumn(format="$%.2f"),
    },
    key="inventory_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.inventory_table.values())

st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.inventory_table),
)


# -----------------------------------------------------------------------------
# Now some cool charts

# Add some space
""
""
""

st.subheader("Units left", divider="red")

need_to_reorder = df[df["units_left"] < df["reorder_point"]].loc[:, "item_name"]

if len(need_to_reorder) > 0:
    items = "\n".join(f"* {name}" for name in need_to_reorder)

    st.error(f"We're running dangerously low on the items below:\n {items}")

""
""

st.altair_chart(
    # Layer 1: Bar chart.
    alt.Chart(df)
    .mark_bar(
        orient="horizontal",
    )
    .encode(
        x="units_left",
        y="item_name",
    )
    # Layer 2: Chart showing the reorder point.
    + alt.Chart(df)
    .mark_point(
        shape="diamond",
        filled=True,
        size=50,
        color="salmon",
        opacity=1,
    )
    .encode(
        x="reorder_point",
        y="item_name",
    ),
    use_container_width=True,
)

st.caption("NOTE: The :diamonds: location shows the reorder point.")

""
""
""

# -----------------------------------------------------------------------------

st.subheader("Best sellers", divider="orange")

""
""

st.altair_chart(
    alt.Chart(df)
    .mark_bar(orient="horizontal")
    .encode(
        x="units_sold",
        y=alt.Y("item_name").sort("-x"),
    ),
    use_container_width=True,
)
