from pyodbc import IntegrityError

from Model.Connection import Connection


class OrderDtlPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_order_data(self,order_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT P.Type,P.Name,P.Color,S.Serial_number,D.Count,D.Price 
        FROM tbl_Order_dtl D
        JOIN tbl_Product P ON P.Product_ID = D.Product_ID
        LEFT JOIN tbl_Serial S ON S.Serial_ID = D.Serial_ID 
        WHERE D.Order_id = ?
        ORDER BY P.Type,P.Name,P.Color
        """, (order_id,))

        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def fetch_suggestions(self,order_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT S.Serial_number
        FROM tbl_Serial S
        join tbl_Order_dtl D
        on S.Serial_ID = D.Serial_ID
        WHERE D.Order_id = ?
        """,(order_id,))

        result = cursor.fetchall()
        cursor.close()
        return [row[0] for row in result]

    def change_status(self,order_id,status):
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE tbl_Order
        SET Status = ?
        WHERE Order_id = ?
        """,(status,order_id))

        self.conn.commit()
        cursor.close()

    def fetch_distinct_values(self,column_name):
        cursor = self.conn.cursor()

        cursor.execute(f"""
        SELECT DISTINCT {column_name} 
        FROM tbl_Product
        """)
        list_distinct = cursor.fetchall()
        result = [i[0] for i in list_distinct]

        cursor.close()
        return result

    def search(self,serial_serial):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT P.Type,P.Name,P.Color,S.Serial_number,D.Price,D.Count 
        FROM tbl_Order_dtl D
        JOIN tbl_Product P ON P.Product_ID = D.Product_ID
        LEFT JOIN tbl_Serial S ON S.Serial_ID = D.Serial_ID
        WHERE S.Serial_number=?
        """,(serial_serial,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self,order_id, product_type, product_name, product_color, serial_serial, product_count):
        cursor = self.conn.cursor()

        product_id , product_price = self.get_product_id(cursor, product_type,product_name,product_color)
        if product_id is None:
            return "No product found",0

        if serial_serial is not None:
            serial_id = self.get_serial_id(cursor, serial_serial)
        else:
            serial_id = None

        try:
            cursor.execute("""
            INSERT INTO tbl_Order_dtl
            (Order_ID,Product_ID,Serial_ID,Count,Price)
            VALUES (?,?,?,?,?)
            """, (order_id,product_id, serial_id, product_count, product_price))

            if serial_id is not None:
                cursor.execute("""
                UPDATE tbl_Serial
                SET Status = 'Sold'
                WHERE Serial_ID = ?
                """, (serial_id,))

            self.conn.commit()
            return "Insert successful",1

        except IntegrityError:
            self.conn.rollback()
            return "product exists",0

        finally:
            cursor.close()

    def remove(self,order_id,product_type,product_name,product_color,serial_serial):
        cursor = self.conn.cursor()

        product_id , _ = self.get_product_id(cursor, product_type,product_name,product_color)
        if product_id is None:
            return "No product found",0

        if serial_serial is not None:
            serial_id = self.get_serial_id(cursor, serial_serial)
        else:
            serial_id = None

        cursor.execute("""
        DELETE FROM tbl_Order_dtl
        WHERE Order_ID=?
        AND Product_ID=?
        AND (Serial_ID=? OR (Serial_ID IS NULL AND ? IS NULL))
        """,(order_id,product_id,serial_id,serial_id))

        if cursor.rowcount == 0:
            cursor.close()
            return "No product found",0

        if serial_id is not None:
            cursor.execute("""
            UPDATE tbl_Serial
            SET Status = 'Available'
            WHERE Serial_ID = ?
            """, (serial_id,))

        self.conn.commit()
        cursor.close()
        return "Remove successful",1

    def adv_search(self, order_id, product_type, product_name, product_color):
        cursor = self.conn.cursor()

        command_list = [["P.Name=?", product_name], ["P.Color=?", product_color]]
        value_list = [order_id,product_type]
        conditions_string = """
        SELECT P.Type,P.Name,P.Color,S.Serial_number,D.Price,D.Count 
        FROM tbl_Order_dtl D
        JOIN tbl_Product P ON P.Product_ID = D.Product_ID
        LEFT JOIN tbl_Serial S ON S.Serial_ID = D.Serial_ID
        where D.Order_ID=?
        AND P.Type=?
        """
        for condition, value in command_list:
            if value is not None:
                conditions_string += f" AND {condition}"
                value_list.append(value)

        conditions_string += " ORDER BY P.Type,P.Name,P.Color"

        cursor.execute(conditions_string,value_list)
        result = cursor.fetchall()

        cursor.close()
        return result

    def fetch_comboboxes_items(self,product_type):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT Name, Color
        FROM tbl_product
        WHERE Type = ?
        """, (product_type,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))))

    @staticmethod
    def get_product_id(cursor, product_type,product_name,product_color):
        cursor.execute("""
        SELECT Product_ID, Price
        FROM tbl_Product
        WHERE Type=?
        AND Name=?
        AND (Color=? OR (Color IS NULL AND ? IS NULL))
        """,(product_type,product_name,product_color,product_color))

        result = cursor.fetchone()
        return result[0] if result is not None else None ,result[1] if result is not None else None

    @staticmethod
    def get_serial_id(cursor, serial_serial):
        cursor.execute("""
        SELECT Serial_ID
        FROM tbl_Serial
        WHERE Serial_number=?
        """,(serial_serial,))

        result = cursor.fetchone()
        return result[0] if result is not None else None