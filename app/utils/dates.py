from datetime import date,datetime




def parse_date_from_folder(folder_name: str) -> datetime.date:
 
    return datetime.strptime(folder_name, "%d.%m.%Y").date()