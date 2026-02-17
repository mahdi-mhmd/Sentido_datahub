from Model.Connection import Connection
from pyodbc import IntegrityError


class ECPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Type,Part_number,Marking,Footprint,Manufacturer,Quantity,Price,Comment
        FROM tbl_EC
        ORDER BY Type
        """)
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def fetch_distinct_values(self,column_name):
        cursor = self.conn.cursor()

        cursor.execute(f"""
        SELECT DISTINCT {column_name} 
        FROM tbl_EC
        ORDER BY {column_name}
        """)
        list_distinct = cursor.fetchall()
        result = [i[0] for i in list_distinct]

        cursor.close()
        return result

    def search(self,ec_part_number):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Type,Part_number,Marking,Footprint,Manufacturer,Quantity,Price,Comment
        FROM tbl_EC
        WHERE Part_number=?
        """,(ec_part_number,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self,ec_type,ec_part_number,ec_marking,ec_footprint,ec_manufacturer,ec_quantity,ec_price,ec_comment):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO tbl_EC 
            (Type,Part_number,Marking,Footprint,Manufacturer,Quantity,Price,Comment)
            VALUES (?,?,?,?,?,?,?,?)
            """,(ec_type,ec_part_number,ec_marking,ec_footprint,ec_manufacturer,ec_quantity,ec_price,ec_comment))

            self.conn.commit()
            return "Insert successful", 1

        except IntegrityError:
            self.conn.rollback()
            return "Component exists", 0

        finally:
            cursor.close()

    def remove(self,ec_type,ec_part_number,ec_marking,ec_footprint,ec_manufacturer):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            DELETE FROM tbl_EC
            WHERE Type=?
            AND Part_number=?
            AND (Marking = ? OR (Marking IS NULL AND ? IS NULL))
            AND (Footprint = ? OR (Footprint IS NULL AND ? IS NULL))
            AND (Manufacturer = ? OR (Manufacturer IS NULL AND ? IS NULL))
            """,(ec_type, ec_part_number,ec_marking,ec_marking ,ec_footprint,ec_footprint, ec_manufacturer,ec_manufacturer))

            if cursor.rowcount == 0:
                return "No component found" , 0

            self.conn.commit()
            return "Remove successful", 1

        except IntegrityError:
            self.conn.rollback()
            return "a reference exists in LOM table", 0

        finally:
            cursor.close()

    def adv_search(self, ec_type, ec_part_number, ec_marking, ec_footprint, ec_manufacturer):
        cursor = self.conn.cursor()

        command_list = [["Part_number=?", ec_part_number], ["Marking=?", ec_marking], ["Footprint=?", ec_footprint], ["Manufacturer=?", ec_manufacturer]]
        value_list = [ec_type]
        conditions_string = """
        SELECT Type,Part_number,Marking,Footprint,Manufacturer,Quantity,Price,Comment
        FROM tbl_EC
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

    def edit_data(self,current_row,new_row):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            UPDATE tbl_EC
            SET Type=?,Part_number=?,Marking=?,Footprint=?,Manufacturer=?,Quantity=?,Price=?,Comment=?
            WHERE Type=?
            AND Part_number=?
            AND (Marking = ? OR (Marking IS NULL AND ? IS NULL))
            AND (Footprint = ? OR (Footprint IS NULL AND ? IS NULL))
            AND (Manufacturer = ? OR (Manufacturer IS NULL AND ? IS NULL))
            """,
            (new_row[0],new_row[1],new_row[2],new_row[3],new_row[4],new_row[5],new_row[6],new_row[7],
            current_row[0],current_row[1],current_row[2],current_row[2],current_row[3],current_row[3],current_row[4],current_row[4]))

            self.conn.commit()
            return "Edit successful", 1

        except IntegrityError:
            self.conn.rollback()
            return "Component exists",0

        finally:
            cursor.close()

    def fetch_comboboxes_items(self,ec_type):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        Part_number, Marking, Footprint, Manufacturer
        FROM tbl_EC
        WHERE Type = ?
        """,(ec_type,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))),
                sorted(list(set([i[2] for i in rows if i[2] is not None]))),
                sorted(list(set([i[3] for i in rows if i[3] is not None]))))