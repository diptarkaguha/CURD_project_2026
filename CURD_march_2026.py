# Database connection details
import mysql.connector

conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ivaan@1905",
    database="curd_1_db")
cur_obj = conn_obj.cursor()


# Define function data_entry_sql
def data_entry_sql(full_name, address, phone_number, user_id, user_pwd):
    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO cust_details (full_name,address,ph_no,user_id,user_pwd) VALUES (%s, %s, %s, %s, %s)"
    data = (full_name, address, phone_number, user_id, user_pwd)

    try:
        cur_obj.execute(sql, data)
        print("Registration SUCCESSFUL!!.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error inserting data to MySQL database:", e)
        conn_obj.rollback()


# Define function data_retrieve
def data_retrieve(user_id_login):
    query = f"select * from cust_details WHERE user_id=\'{user_id_login}\'";

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result;


def new_user_creation():
    full_name = input("Please enter your full name: ").strip().upper();
    address = input("Please enter your address: ").strip().upper();
    phone_number = input("Please enter your phone number: ");
    while True:
        user_id = input("Please enter your user ID: ");
        result_from_db = data_retrieve(user_id);
        if not (result_from_db):
            user_pwd = input("Please enter your password: ");
            data_entry_sql(full_name, address, phone_number, user_id, user_pwd);
            break
        else:
            print("user id already exist, please try another user id")


def delete_data(user_id_login):
    # Build the query with user-provided name using LIKE operator
    # delete from cust_details where user_id is provided;
    query = f"delete from cust_details where user_id=\'{user_id_login}\'"

    try:
        cur_obj.execute(query)
        print("RECORD HAS BEEN REMOVED for the user", user_id_login)
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()


def update_user_option(user_id_login):
    print("What do you want to update?")
    print("1. address")
    print("2. Phone Number")
    print("3. Password")

    option = input("Select option: ")

    try:

        if option == "1":
            new_address = input("Enter new address: ")
            query = "UPDATE cust_details SET address=%s WHERE user_id=%s"
            cur_obj.execute(query,(new_address, user_id_login))

        elif option == "2":
            new_phone_number = input("Enter new phone number: ")
            query = "UPDATE cust_details SET ph_no=%s WHERE user_id=%s"
            cur_obj.execute(query,(new_phone_number, user_id_login))

        elif option == "3":
            new_user_pwd = input("Enter new password: ")
            query = "UPDATE cust_details SET user_pwd=%s WHERE user_id=%s"
            cur_obj.execute(query,(new_user_pwd, user_id_login))



        else:
            print("Invalid option")
            return

        conn_obj.commit()
        print("Record updated successfully")

    except mysql.connector.Error as e:
        print("Error updating record:", e)
        conn_obj.rollback()


##main logic starts from here
print("welcome to demo login app");
print("select from below option")
res = input("1. new user creation\n2.existing user login\n3.removal of user\n4.updation of user\n-->");
if res == "1":
    new_user_creation();
elif res == "2":
    pass
    user_id_login = input("Please enter your user ID: ");
    result_from_db = data_retrieve(user_id_login);
    if result_from_db:
        user_pwd_login = input("Please enter your password: ");
        cust_pwd = result_from_db[5]
        if cust_pwd == user_pwd_login:
            print("access granted!!")
            print("Please check your details::")
            for details in result_from_db:
                print(f"-->{details}")
        else:
            print("wrong input !! please try again")
    else:
        print("user id does not exist !! Please register first")
        new_user_creation();

elif res == "3":
    pass
    user_id_login = input("Please enter your user ID: ");
    delete_data(user_id_login);

elif res == "4":
    pass
    user_id_login = input("Please enter your user ID: ");
    update_user_option(user_id_login);
    print("updated the details successfully !!");
else:
    print("please select from below option");
conn_obj.close()