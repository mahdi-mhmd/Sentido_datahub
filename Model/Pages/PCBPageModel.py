from pyodbc import IntegrityError

from Model.Connection import Connection


class PCBPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Name,[Board/sheet],Color,Finishing,Thickness,Sheet_Qty,Board_Qty,Price,Comment
        FROM tbl_PCB
        ORDER BY Name
        """)
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def fetch_distinct_values(self,column_name):
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT DISTINCT {column_name}
        FROM tbl_PCB
        """)
        list_distinct = cursor.fetchall()
        result = [i[0] for i in list_distinct]

        cursor.close()
        return result

    def search(self, pcb_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Name,[Board/sheet],Color,Finishing,Thickness,Sheet_Qty,Board_Qty,Price,Comment
        FROM tbl_PCB
        WHERE Name=?
        """, (pcb_name,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self, pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness, pcb_sheet_qty, pcb_price, pcb_comment):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO tbl_PCB 
            (Name,[Board/sheet],Color,Finishing,Thickness,Sheet_Qty,Price,Comment)
            VALUES (?,?,?,?,?,?,?,?)
            """, (pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness, pcb_sheet_qty, pcb_price, pcb_comment))

            self.conn.commit()
            return "Insert successful",1

        except IntegrityError:
            self.conn.rollback()
            return "PCB exists",0

        finally:
            cursor.close()

    def remove(self, pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            DELETE FROM tbl_PCB
            WHERE Name=?
            AND [Board/sheet]=?
            AND (Color = ? OR (Color IS NULL AND ? IS NULL))
            AND (Finishing = ? OR (Finishing IS NULL AND ? IS NULL))
            AND (Thickness = ? OR (Thickness IS NULL AND ? IS NULL))
            """, (pcb_name, pcb_board_per_sheet, pcb_color, pcb_color , pcb_finishing, pcb_finishing, pcb_thickness, pcb_thickness))

            if cursor.rowcount == 0:
                return "No PCB found",0

            self.conn.commit()
            return "Remove successful",1

        except IntegrityError:
            self.conn.rollback()
            return "a reference exists in LOM table", 0

        finally:
            cursor.close()

    def adv_search(self, pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness):
        cursor = self.conn.cursor()

        command_list = [["[Board/sheet]=?", pcb_board_per_sheet], ["Color=?", pcb_color], ["Finishing=?", pcb_finishing], ["Thickness=?", pcb_thickness]]
        value_list = [pcb_name]
        conditions_string = """
        SELECT Name,[Board/sheet],Color,Finishing,Thickness,Sheet_Qty,Board_Qty,Price,Comment
        FROM tbl_PCB
        WHERE Name=?
        """
        for condition, value in command_list:
            if value is not None:
                conditions_string += f" AND {condition}"
                value_list.append(value)

        cursor.execute(conditions_string,value_list)
        result = cursor.fetchall()

        cursor.close()
        return result

    def fetch_comboboxes_items(self, pcb_name):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        [Board/sheet],Color,Finishing,Thickness
        FROM tbl_PCB
        WHERE Name = ?
        """,(pcb_name,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))),
                sorted(list(set([i[2] for i in rows if i[2] is not None]))),
                sorted(list(set([i[3] for i in rows if i[3] is not None]))))

    def edit_data(self,current_row,new_row):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            UPDATE tbl_PCB
            SET Name=?,[Board/sheet]=?,Color=?,Finishing=?,Thickness=?,Sheet_Qty=?,Price=?,Comment=?
            WHERE Name=?
            AND [Board/sheet]=?
            AND (Color = ? OR (Color IS NULL AND ? IS NULL))
            AND (Finishing = ? OR (Finishing IS NULL AND ? IS NULL))
            AND (Thickness = ? OR (Thickness IS NULL AND ? IS NULL))
            """,
            (new_row[0],new_row[1],new_row[2],new_row[3],new_row[4],new_row[5],new_row[6],new_row[7],
            current_row[0],current_row[1],current_row[2],current_row[2],current_row[3],current_row[3],current_row[4],current_row[4]))
            self.conn.commit()
            return "Edit successful",1

        except IntegrityError:
            self.conn.rollback()
            return "PCB exists",0

        finally:
            cursor.close()
