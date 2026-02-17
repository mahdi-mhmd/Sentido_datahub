from pyodbc import IntegrityError

from Model.Connection import Connection


class ProductPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Type,Name,Color,Quantity,Price,Comment
        FROM tbl_Product
        ORDER BY Type
        """)
        result = cursor.fetchall()

        cursor.close()
        return list(result)

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

    def search(self,product_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Type,Name,Color,Quantity,Price,Comment
        FROM tbl_Product
        WHERE Name=?
        """,(product_name,))
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def insert(self,product_type,product_name,product_color,product_qty,product_price,product_comment):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO tbl_Product 
            (Type,Name,Color,Quantity,Price,Comment)
            VALUES (?,?,?,?,?,?)
            """,(product_type,product_name,product_color,product_qty,product_price,product_comment))

            self.conn.commit()
            return "Insert successful",1

        except IntegrityError:
            self.conn.rollback()
            return "product Exists",0

        finally:
            cursor.close()

    def remove(self,product_type,product_name,product_color):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            DELETE FROM tbl_Product
            WHERE Type=?
            AND Name=?
            AND (Color = ? OR (Color IS NULL AND ? IS NULL))
            """,(product_type, product_name,product_color,product_color))

            if cursor.rowcount == 0:
                return "No product found",0

            self.conn.commit()
            return "Remove successful",1

        except IntegrityError:
            self.conn.rollback()
            return "a reference exists in Serial/Order table", 0

        finally:
            cursor.close()

    def adv_search(self, product_type, product_name, product_color):
        cursor = self.conn.cursor()

        command_list = [["Name=?", product_name], ["Color=?", product_color]]
        value_list = [product_type]
        conditions_string = """
        SELECT Type,Name,Color,Quantity,Price,Comment
        FROM tbl_Product
        WHERE Type=?
        """
        for condition, value in command_list:
            if value is not None:
                conditions_string += f" AND {condition}"
                value_list.append(value)

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

        try:
            cursor.execute("""
            UPDATE tbl_Product
            SET Type=?,Name=?,Color=?,Quantity=?,Price=?,Comment=?
            WHERE Type=?
            AND Name=?
            AND (Color = ? OR (Color IS NULL AND ? IS NULL))
            """,
            (new_row[0],new_row[1],new_row[2],new_row[3],new_row[4],new_row[5],
            current_row[0],current_row[1],current_row[2],current_row[2]))
            self.conn.commit()
            return "Edit successful",1

        except IntegrityError:
            self.conn.rollback()
            return "product exists",0

        finally:
            cursor.close()
