from typing import List

import pandas as pd

from application.db_app.schemas import MenuParseSchema, SubmenuParseSchema, DishParseSchema


class XlsxDataSource:
    def __init__(self, filename: str):
        self.filename = filename
        self.menus_file_data = []
        self.submenus_file_data = []
        self.dishes_file_data = []
        self.parse()

    def parse(self) -> List:
        df = pd.DataFrame(data=pd.read_excel(self.filename, header=None))
        current_menu_id = None
        current_submenu_id = None
        result = []
        for index, row in df.iterrows():

            if pd.notna(row[0]):
                current_menu_id = row[0]
                self.menus_file_data.append(MenuParseSchema(id=int(row[0]), title=row[1], description=row[2]))

            elif pd.notna(row[1]):
                if current_menu_id is None:
                    raise Exception("Unexpected Submenu without Menu. Row index:", index)
                current_submenu_id = row[1]
                self.submenus_file_data.append(
                    SubmenuParseSchema(id=int(row[1]), title=row[2], description=row[3], menu_id=int(current_menu_id)))

            elif pd.notna(row[2]):
                if current_submenu_id is None:
                    raise Exception("Unexpected Dish without Submenu. Row index:", index)
                self.dishes_file_data.append(
                    DishParseSchema(id=int(row[2]), title=row[3], description=row[4], price=str(row[5]),
                                    submenu_id=int(current_submenu_id), menu_id=int(current_menu_id)))

            else:
                print('Unexpected line', row)

        return result