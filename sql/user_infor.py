# importing sqlite3 module
import sqlite3


# create connection by using object
# to connect with hotel_data database

def main():
    connection = sqlite3.connect('./sql/user_data.db')
    connection.execute(''' CREATE TABLE user
		(USERID TEXT PRIMARY KEY	 NOT NULL,
		FNAME		 TEXT NOT NULL,
		EMAIL		 TEXT NOT NULL);
		''')
    connection.close()
    
def insert(userID, name, email):
    connection = sqlite3.connect('./sql/user_data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user (USERID, FNAME, EMAIL) VALUES (?, ?, ?)", (userID, name, email))

    connection.commit()

    cursor.close()
    connection.close()
     
	
def search_user(userID):
    # Create a new connection
    connection = sqlite3.connect("./sql/user_data.db")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE USERID = ?", (userID,))
    result = cursor.fetchone()

    if result is None:
        print("No user found.")
    else:
        print("User found.")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return result



# insert query to insert food details in 
# the above table
if __name__ == "__main__":
    main()
