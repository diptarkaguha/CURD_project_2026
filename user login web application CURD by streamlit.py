import streamlit as st
import mysql.connector

# Database connection
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ivaan@1905",
    database="curd_1_db"
)

cur_obj = conn_obj.cursor()


# ---------------- DATABASE FUNCTIONS (UNCHANGED LOGIC) ---------------- #

def data_entry_sql(full_name, address, phone_number, user_id, user_pwd):

    sql = "INSERT INTO cust_details (full_name,address,ph_no,user_id,user_pwd) VALUES (%s, %s, %s, %s, %s)"
    data = (full_name, address, phone_number, user_id, user_pwd)

    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
        st.success("Registration SUCCESSFUL!!")

    except mysql.connector.Error as e:
        st.error(f"Error inserting data: {e}")
        conn_obj.rollback()


def data_retrieve(user_id_login):

    query = f"select * from cust_details WHERE user_id='{user_id_login}'"

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
        return result

    except mysql.connector.Error as e:
        st.error(f"Error retrieving data: {e}")
        conn_obj.rollback()


def delete_data(user_id_login):

    query = f"delete from cust_details where user_id='{user_id_login}'"

    try:
        cur_obj.execute(query)
        conn_obj.commit()
        st.success(f"RECORD HAS BEEN REMOVED for user {user_id_login}")

    except mysql.connector.Error as e:
        st.error(f"Error deleting data: {e}")
        conn_obj.rollback()


def update_user_option(user_id_login, option, value):

    try:

        if option == "address":
            query = "UPDATE cust_details SET address=%s WHERE user_id=%s"
            cur_obj.execute(query, (value, user_id_login))

        elif option == "phone":
            query = "UPDATE cust_details SET ph_no=%s WHERE user_id=%s"
            cur_obj.execute(query, (value, user_id_login))

        elif option == "password":
            query = "UPDATE cust_details SET user_pwd=%s WHERE user_id=%s"
            cur_obj.execute(query, (value, user_id_login))

        conn_obj.commit()
        st.success("Record updated successfully")

    except mysql.connector.Error as e:
        st.error(f"Error updating record: {e}")
        conn_obj.rollback()


# ---------------- STREAMLIT UI ---------------- #

st.title("Demo Login App")

option = st.sidebar.selectbox(
    "Select Option",
    ("New User Creation", "Existing User Login", "Removal of User", "Updation of User")
)

# -------- NEW USER -------- #

if option == "New User Creation":

    st.header("Register New User")

    full_name = st.text_input("Full Name")
    address = st.text_input("Address")
    phone = st.text_input("Phone Number")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Register"):

        result_from_db = data_retrieve(user_id)

        if not result_from_db:
            data_entry_sql(full_name.strip().upper(),
                           address.strip().upper(),
                           phone,
                           user_id,
                           password)
        else:
            st.warning("User ID already exists. Try another.")


# -------- LOGIN -------- #

elif option == "Existing User Login":

    st.header("Login")

    user_id_login = st.text_input("User ID")
    user_pwd_login = st.text_input("Password", type="password")

    if st.button("Login"):

        result_from_db = data_retrieve(user_id_login)

        if result_from_db:

            cust_pwd = result_from_db[4]

            if cust_pwd == user_pwd_login:

                st.success("Access granted!!")
                st.write("User Details:")

                for details in result_from_db:
                    st.write(details)

            else:
                st.error("Wrong password")

        else:
            st.warning("User ID does not exist. Please register first.")


# -------- DELETE USER -------- #

elif option == "Removal of User":

    st.header("Delete User")

    user_id_login = st.text_input("Enter User ID")

    if st.button("Delete"):

        delete_data(user_id_login)


# -------- UPDATE USER -------- #

elif option == "Updation of User":

    st.header("Update User Details")

    user_id_login = st.text_input("User ID")

    update_option = st.selectbox(
        "Select Field to Update",
        ("address", "phone", "password")
    )

    new_value = st.text_input("Enter New Value")

    if st.button("Update"):

        update_user_option(user_id_login, update_option, new_value)