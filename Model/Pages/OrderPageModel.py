from Model.Connection import Connection
from persiantools.jdatetime import JalaliDate
from datetime import datetime

class OrderPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT C.Name,C.Tel,C.City,C.Address,O.date,O.Status,O.Order_ID,O.Comment
        FROM tbl_Order O
        JOIN tbl_Customer C ON O.Customer_ID = C.Customer_ID
        ORDER BY C.Name
        """)
        rows = cursor.fetchall()
        cursor.close()
        result = []

        for row in rows:
            g_date = row[4]
            if isinstance(g_date, str):
                g_date = datetime.strptime(g_date, "%Y-%m-%d").date()

            p_date = JalaliDate.to_jalali(g_date).strftime("%Y/%m/%d")
            result.append((row[0],row[1],row[2],row[3],p_date,row[5],row[6],row[7]))

        return result

    def fetch_distinct_values(self,column_name):
        cursor = self.conn.cursor()

        cursor.execute(f"""
        SELECT DISTINCT {column_name} 
        FROM tbl_Customer
        """)
        list_distinct = cursor.fetchall()
        result = [i[0] for i in list_distinct]

        cursor.close()
        return result

    def search(self,customer_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT C.Name,C.Tel,C.City,C.Address,O.date,O.Status,O.Order_ID,O.Comment
        FROM tbl_Order O
        JOIN tbl_Customer C ON O.Customer_ID = C.Customer_ID
        WHERE C.Name=?
        """,(customer_name,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self,customer_name,customer_tel,customer_city,customer_address,order_date,order_comment):
        cursor = self.conn.cursor()

        customer_id = self.get_customer_id(cursor,customer_name,customer_tel,customer_city,customer_address)
        if customer_id is None:
            cursor.close()
            return "Customer not found",0

        cursor.execute("""
        INSERT INTO tbl_Order
        (Customer_ID,[date],Comment)
        VALUES (?,?,?)
        """,(customer_id,order_date,order_comment))
        self.conn.commit()
        cursor.close()
        return "Insert successful",1

    def remove(self,order_id):
        cursor = self.conn.cursor()

        cursor.execute("""
        DELETE FROM tbl_Order
        WHERE Order_ID=?
        """,(order_id,))

        if cursor.rowcount == 0:
            cursor.close()
            return "Order not found",0

        self.conn.commit()
        cursor.close()
        return "Remove successful",1

    def adv_search(self,customer_name, customer_tel, customer_city):
        cursor = self.conn.cursor()

        command_list = [["C.Name=?",customer_name],["C.Tel=?", customer_tel],["C.City=?", customer_city]]
        value_list = []
        conditions_string = """
        SELECT C.Name,C.Tel,C.City,C.Address,O.date,O.Status,O.Order_ID,O.Comment
        FROM tbl_Order O
        JOIN tbl_Customer C ON O.Customer_ID = C.Customer_ID
        WHERE 1=1
        """
        for condition, value in command_list:
            if value is not None:
                conditions_string += f" AND {condition}"
                value_list.append(value)

        conditions_string += " ORDER BY C.Name"

        cursor.execute(conditions_string,value_list)
        result = cursor.fetchall()

        cursor.close()
        return result

    def fetch_comboboxes_items(self,customer_name):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        Tel,City,Address
        FROM tbl_Customer
        WHERE Name = ?
        """,(customer_name,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))),
                sorted(list(set([i[2] for i in rows if i[2] is not None]))))

    @staticmethod
    def get_customer_id(cursor, customer_name,customer_tel,customer_city,customer_address):
        cursor.execute("""
        SELECT Customer_ID
        FROM tbl_Customer
        WHERE Name = ?
        AND Tel = ?
        AND City = ?
        AND Address = ?
        """, (customer_name,customer_tel,customer_city,customer_address))

        result = cursor.fetchone()
        return result[0] if result is not None else None