from pyodbc import IntegrityError

from Model.Connection import Connection


class SerialPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT P.Type,P.Name,P.Color,S.Serial_number,S.Mac_address,S.Status,S.Comment
        FROM tbl_Serial S 
        JOIN tbl_Product P 
        ON S.Product_ID=P.Product_ID
        ORDER BY S.Status,P.Type,P.Name,P.Color
        """)
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def fetch_suggestions(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Serial_number
        FROM tbl_Serial
        """)
        result = cursor.fetchall()

        cursor.close()
        return [row[0] for row in result]

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
        SELECT P.Type, P.Name, P.Color, S.Serial_number, S.Mac_address,S.Status ,S.Comment
        FROM tbl_Serial S
        JOIN tbl_Product P
        ON S.Product_ID = P.Product_ID
        WHERE S.Serial_number=?
        ORDER BY S.Status, P.Type, P.Name, P.Color
        """,(serial_serial,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self, product_type, product_name, product_color, serial_serial, serial_mac, serial_comment):
        cursor = self.conn.cursor()

        product_id = self.get_product_id(cursor, product_type, product_name, product_color)
        if product_id is None:
            return "no product found",0

        try:
            cursor.execute("""
            INSERT INTO tbl_Serial
            (Product_ID,Serial_number,Mac_address,Status,Comment)
            VALUES (?,?,?,DEFAULT,?)
            """, (product_id, serial_serial, serial_mac, serial_comment))

            self.conn.commit()
            return "Insert successful",1

        except IntegrityError:
            self.conn.rollback()
            return "Serial exists",0

        finally:
            cursor.close()

    def remove(self,product_type,product_name,product_color,serial_serial):
        cursor = self.conn.cursor()

        try:
            product_id = self.get_product_id(cursor,product_type,product_name,product_color)

            cursor.execute("""
            DELETE FROM tbl_Serial
            WHERE Product_ID=?
            AND Serial_number=?
            """,(product_id,serial_serial))

            if cursor.rowcount == 0:
                return "No Serial found",0

            self.conn.commit()
            return "Remove successful",1

        except IntegrityError:
            self.conn.rollback()
            return "a reference exists in Order table", 0

        finally:
            cursor.close()

    def adv_search(self, product_type, product_name, product_color):
        cursor = self.conn.cursor()

        command_list = [["Name=?", product_name], ["Color=?", product_color]]
        value_list = [product_type]
        conditions_string = """
        SELECT P.Type,P.Name,P.Color,S.Serial_number,S.Mac_address,S.Status,S.Comment
        FROM tbl_Serial S 
        JOIN tbl_Product P 
        ON S.Product_ID = P.Product_ID
        WHERE Type=?
        """
        for condition, value in command_list:
            if value is not None:
                conditions_string += f" AND {condition}"
                value_list.append(value)

        conditions_string += " ORDER BY S.Status,P.Name,P.Color"

        cursor.execute(conditions_string,value_list)
        result = cursor.fetchall()

        cursor.close()
        return result

    def fetch_comboboxes_items(self,product_type):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        Name,Color
        FROM tbl_product
        WHERE Type = ?
        """,(product_type,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))))

    def edit_data(self,current_row,new_row):
        cursor = self.conn.cursor()
        product_id = self.get_product_id(cursor, current_row[0], current_row[1], current_row[2])
        new_product_id = self.get_product_id(cursor, new_row[0][0], new_row[0][1], new_row[0][2])

        try:
            cursor.execute("""
            UPDATE tbl_Serial
            SET Product_ID=?,Serial_number=?,Mac_address=?,Status=?,Comment=?
            WHERE Product_ID=?
            AND Serial_number=?
            """,
            (new_product_id,new_row[1][0],new_row[1][1],new_row[1][2],new_row[1][3],
            product_id,current_row[3]))

            self.conn.commit()
            return "Edit successful",1

        except IntegrityError:
            self.conn.rollback()
            return "Serial exists",0

        finally:
            cursor.close()

    @staticmethod
    def get_product_id(cursor, product_type,product_name,product_color):
        cursor.execute("""
        SELECT Product_ID
        FROM tbl_Product
        WHERE Type=?
        AND Name=?
        AND (Color=? OR (Color IS NULL AND ? IS NULL))
        """,(product_type,product_name,product_color,product_color))

        result = cursor.fetchone()
        return result[0] if result is not None else None