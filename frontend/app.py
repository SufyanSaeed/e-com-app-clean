import streamlit as st
import api_client
import json

st.title("🛒 E-commerce Frontend")


if "page" not in st.session_state:
    st.session_state["page"] = "Login"
if "cart" not in st.session_state:
    st.session_state["cart"] = []
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ---------- SIDEBAR MENU ----------
if st.session_state["logged_in"]:
    menu = ["Products", "View Cart", "Checkout", "My Orders", "Logout"]
else:
    menu = ["Signup", "Login","Products"]

# Sidebar selectbox with current index
current_index = menu.index(st.session_state["page"]) if st.session_state["page"] in menu else 0
choice = st.sidebar.selectbox("Menu", menu, index=current_index)

# Save choice in session_state
st.session_state["page"] = choice


# ----------------- SIGNUP -----------------
if choice == "Signup":
    st.subheader("Create Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        r = api_client.register(username, email, password)
        if r.status_code in [200, 201]:
            st.success("✅ Account created successfully! Please log in.")
        else:
            st.error(f"❌ {r.json().get('detail', 'Registration failed')}")


# ----------------- LOGIN -----------------
elif choice == "Login":
    st.subheader("Login to your account")
    username = st.text_input("User Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        r = api_client.login(username, password)
        if r.status_code == 200:
            token_data = r.json()
            st.session_state["token"] = token_data["access_token"]
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("✅ Logged in successfully!")

            # Check if admin
            st.session_state["is_admin"] = api_client.is_admin(username)
            st.session_state["page"] = "Products"   # redirect to products
            st.rerun()
        else:
            st.error(f"❌ {r.json().get('detail', 'Invalid credentials')}")


# ----------------- PRODUCTS -----------------
elif choice == "Products":
    st.subheader("Products")
    items = api_client.get_products()
    if isinstance(items, list):
        for item in items:
            st.markdown(f"**{item['name']}** - 💲{item['price']} - Qty: {item['quantity_available']}")

            if st.session_state.get("logged_in"):
                col1, col2 = st.columns([1,1])
                with col1:
                    required_quantity = st.number_input(
                        f"Quantity for {item['name']}",
                        min_value=1,
                        step=1,
                        key=f"qty_{item['id']}"
                    )
                with col2:
                    if st.button(f"Add to Cart - {item['id']}", key=f"add_{item['id']}"):
                        payload = {"name": item['name'], "quantity": required_quantity}
                        cart_item = api_client.add_to_cart(payload, st.session_state["token"])
                        st.success(f"{item['name']} added to cart!")
            else:
                st.caption("🔒 Login to add this item to your cart.")
    else:
        st.warning("⚠️ Could not fetch items.")


# ----------------- VIEW CART -----------------
elif choice == "View Cart":
    st.subheader("🛒 Your Cart")
    r = api_client.view_cart(st.session_state["token"])

    if r.status_code == 200:
        data = r.json()
        items = data.get("cart_items", [])

        if items:
            for item in items:
                st.markdown(
                    f"**{item['name']}** - $ {item['total_price']} - Qty: {item['quantity']}"
                )
        else:
            st.info("🛒 Your cart is empty.")
    else:
        st.error("❌ Failed to load cart.")


# -------------------Checkout---------------------
elif choice == "Checkout":
    st.subheader("Checking Out")
    if st.session_state.get("logged_in"):
        r = api_client.view_cart(st.session_state["token"])
        data = r.json()
        items = data.get("cart_items", [])
        total_price=0

        if items:
            for item in items:
                st.markdown(
                    f"**{item['name']}** - $ {item['total_price']} - Qty: {item['quantity']}"
                    )
                total_price+=item['total_price']
            
            st.markdown(f"** Total Amount is: {total_price}")
        else:
            st.info("🛒 Your cart is empty.")
        if st.button("Confirm Checkout"):
            r = api_client.checkout(st.session_state["token"])
            if r.status_code == 200:
                st.success("✅ Order placed successfully!")
                st.session_state["cart"] = []  # local cart empty
            else:
                st.error(f"❌ Checkout failed: {r.json().get('detail', 'Unknown error')}")




# ----------------- MY ORDERS -----------------

elif choice == "My Orders":
    st.subheader("📦 My Orders")

    if st.session_state.get("logged_in"):
        r = api_client.myOrders(st.session_state["token"])
        if r.status_code == 200:
            orders = r.json()

            if orders:
                for order in orders:
                    
                    st.markdown(f"👤 **User:** {order['user_id']}")
                    st.markdown(f"💲 **Total Price:** {order['total_bill']}")
                    st.markdown(f"📅 **Date:** {order['placed_at']}")

                    # Parse items JSON string
                    items = order["items"]
                    st.write("🛒 **Items:**")
                    for it in items:
                        st.markdown(
                            f"- Product ID: {it['product_id']} | Qty: {it['quantity']} | Price: {it['price']}"
                        )
                    

                    st.divider()
            else:
                st.info("📭 You have no orders yet.")
        else:
            st.error("❌ Failed to fetch orders.")
    else:
        st.warning("🔒 Please login to view your orders.")
# ----------------- LOGOUT -----------------
elif choice == "Logout":
    st.subheader("Logging Out")
    if st.session_state.get("logged_in"):
        if st.button("Confirm Logout"):
            for key in ["token", "logged_in", "username", "is_admin", "admin_choice"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state["page"] = "Login"
            st.rerun()


# ----------------- ADMIN PANEL -----------------
if st.session_state.get("logged_in") and st.session_state.get("is_admin"):
    st.subheader("Admin Panel")
    admin_options = ["Add Product", "Delete Product", "Update Product"]
    choice = st.sidebar.selectbox("Admin Actions", admin_options, key="admin_actions")
    st.session_state["admin_choice"] = choice

    if choice == "Add Product":
        st.write("Add Product")
        # (same as before...)
