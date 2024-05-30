from tabulate import tabulate
import textwrap
import getpass
import os



class OperationSheet:
    
    def __init__(self) -> None:
        
        # 6. Collaborate with an other user
        
        self.current_user = 'admin'
        self.users = [
            {'user_name': 'admin', 'account': 'admin', 'password': 'admin'}, 
            {'user_name': 'user', 'account': 'user', 'password': 'user'}
        ] 
        self.sheets = [{
            "owner_name": "admin",
            "sheet_name": "sheet_A",
            "user_list": [],
            "content": [[1], [2, 3]]
        }, {
            "owner_name": "user",
            "sheet_name": "sheet_U",
            "user_list": [{ "user_name": "admin", "access_right": "ReadOnly"}],
            "content": []
        }] 
        self.current_sheet_index = None
        
        is_process = True
        while is_process:
            # Print the Menu List to use
            print(textwrap.dedent(f"""
            Hello, Can I help you? {self.current_user or ""}
            ---------------Menu---------------
            1. Create a user.
            2. Login.
            3. Logout.
            4. Create a sheet
            5. Check the sheet 
            6. Access the sheet
            
            0. Exit the program
            ====================================
            """))
            is_process = self.action()

    def action(self):
        select_option = input("Please enter your action option(number please): ")
        if select_option == "1":
            self.create_user()
        elif select_option == "2":
            self.login()
        elif select_option == "3" and self.is_login():
            self.logout()
        elif select_option == "4" and self.is_login():
            self.create_sheet()
        elif select_option == "5"  and self.is_login():
            self.check_sheet()
            sheet_index = input("Please enter the sheet ID number to check the content(-1 to exit.): ")
            self.print_sheet_content(sheet_index)
        elif select_option == "6" and self.is_login():
            self.access_sheet()
        elif select_option == "0":
            return False
        else:
            print("Please enter the correct option!")
            
        input("Press any key to continue...")  # 等待用戶按下隨意鍵
        os.system('cls' if os.name == 'nt' else 'clear')  # 清空終端機畫面
        
        return True

    def create_user(self):
        print(textwrap.dedent("""
        Now have something need you to do:
        Please enter you User Name, Account and Password to create a new user.
        """))
        
        user_name = input("User Name: ")
        account = input("Account: ")
        password = getpass.getpass("Password: ")
        
        # Check the repeated user name and account
        is_double = False
        for user in self.users:
            if user['user_name'] == user_name or user['account'] == account:
                print(f"Already have the user name or account!")
                is_double = True
        
        if is_double == False:
            self.users.append({
                "user_name": user_name,
                "account": account,
                "password": password
            })
            self.current_user = user_name
            print("Create a new user successfully! You are logging now!")
            
    def login(self):
        
        print("Please enter your account and password to login.")
        account = input("Account: ")
        password = input("Password: ")
        
        for user in self.users:
            if user['account'] == account and user['password'] == password:
                self.current_user = user["user_name"]
                print(f"Welcome {user['user_name']} to login!")
                break
            
    def logout(self):
        print("Logout successfully! See you next time, " + str(self.current_user) + " !")
        self.current_user = None

    def create_sheet(self):
        
        sheet_name = input("Please enter the sheet name: ")
        self.sheets.append({
            "owner_name": self.current_user,
            "sheet_name": sheet_name,
            "user_list": [],
            "content": []
        })
        
        print(f"Create a new sheet '{sheet_name}' for {self.current_user} successfully!")
        
    def check_sheet(self, show_user=True):
        
        print()
        for index, sheet in enumerate(self.sheets):
            if sheet['owner_name'] == self.current_user:
                print(f"Sheet ID number: {index}, Sheet Name: {sheet['sheet_name']}")
                
            if show_user:
                for user in sheet['user_list']:
                    if user['user_name'] == self.current_user:
                        print(f"Sheet ID number: {index}, Sheet Name: {sheet['sheet_name']}, Sheet Access Right: {user['access_right']}")
                    
    def access_sheet(self):
        
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            # Print the Sheet Menu List to use
            print(textwrap.dedent(f"""
            Now access in: {self.sheets[self.current_sheet_index]['sheet_name'] if self.current_sheet_index is not None else "None"}
            ---------------Sheet Menu---------------
            1. Select the sheet
            4. change access right of the sheet
            
            # have selected the sheet
            2. Print the sheet content
            3. change_value
            
            0. Exit the Sheet Menu
            ====================================
            """))
            select_option = input("Please enter your action option(number please): ")
            if select_option == "1":
                self.select_sheet()
            elif select_option == "2" and self.is_select_sheet():
                self.print_sheet_content(self.current_sheet_index)
            elif select_option == "3" and self.is_select_sheet():
                self.change_value()
            elif select_option == "4":
                self.change_access_right()
            elif select_option == "0":
                break
            else:
                print("Please enter the correct option!")
                
            input("Press any key to continue...")  # 等待用戶按下隨意鍵
            os.system('cls' if os.name == 'nt' else 'clear')  # 清空終端機畫面
            
    def select_sheet(self):
        self.check_sheet()
        sheet_index = input("Please enter the sheet ID number to check the content(-1 to exit.): ")
        self.print_sheet_content(sheet_index)
        if sheet_index == "-1": 
            self.current_sheet_index = None
            print("Now you are not access any sheet.")
        else:
            self.current_sheet_index = int(sheet_index)
            print("Now you are successfully access the sheet: " + self.sheets[self.current_sheet_index]['sheet_name'])

    def change_value(self):
        
        self.print_sheet_content(self.current_sheet_index)
        row_index = input("Please enter the row number to change the value: ")
        column_index = input("Please enter the column number to change the value: ")
        value = input("Please enter the new value: ")

        try:
            row_index = int(row_index)
            column_index = int(column_index)
            
            # 檢查是否需要新增行
            while row_index >= len(self.sheets[self.current_sheet_index]['content']):
                self.sheets[self.current_sheet_index]['content'].append([])
            
            # 檢查是否需要新增列
            while column_index >= len(self.sheets[self.current_sheet_index]['content'][row_index]):
                self.sheets[self.current_sheet_index]['content'][row_index].append(None)
            
            self.sheets[self.current_sheet_index]['content'][row_index][column_index] = value
            print("Change the value successfully!")
        except ValueError:
            print("Please enter the correct row and column number!")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_sheet_content(self.current_sheet_index)

    def change_access_right(self):
        self.check_sheet(show_user=False)
        sheet_index = input("Please enter the sheet ID number to change the access right(-1 to exit.): ")
        if sheet_index == "-1": return

        print("This is the user list of the sheet:", self.sheets[int(sheet_index)]['user_list'])

        user_name = input("Please enter the user name: ")
        access_right = input("Please enter the access right(ReadOnly, ReadWrite): ")
        if self.is_user_exit_list() == False:
            print("The user is not exist!")
            return
            
        is_user_exist = False
        for user in self.users:
            if user['user_name'] == user_name:
                is_user_exist = True
                break
        
        if is_user_exist == False:
            print("Now we added the user to the user list.")
            self.sheets[int(sheet_index)]['user_list'].append({
                "user_name": user_name,
                "access_right": access_right
            })
        elif is_user_exist:
            print("Now we changed the access right of the user.")
            for user in self.sheets[int(sheet_index)]['user_list']:
                if user['user_name'] == user_name:
                    user['access_right'] = access_right
                    break
                
        print("This is the new user list of the sheet:", self.sheets[int(sheet_index)]['user_list'])
        

    def is_select_sheet(self):
        if self.current_sheet_index is None:
            print("Please select the sheet first!")
            return False
        
        return True

    def is_login(self):
        if self.current_user is None:
            print("Please login first!")
            return False
        
        return True

    def print_sheet_content(self, sheet_index):
        try:
            if sheet_index == "-1" or sheet_index is None:
                return

            sheet = self.sheets[int(sheet_index)]
            if not sheet['content']:
                print("The sheet content is empty.")
                return

            max_cols = max(len(row) for row in sheet['content'])
            for row in sheet['content']:
                row.extend([''] * (max_cols - len(row)))

            headers = [""] + [f"Col {i}" for i in range(max_cols)]
            table = sheet['content']
            table_with_index = [[f"Row {i}"] + row for i, row in enumerate(table)]
            table_with_index.insert(0, headers)

            print(tabulate(table_with_index, headers="firstrow", tablefmt="grid"))
        except:
            print("Please enter the correct sheet ID number!")
            return "-1"

    def is_user_exit_list(self, user_name):
        is_exit = False
        for user in self.users:
            if user['user_name'] == user_name:
                is_exit = True
                break
        return is_exit
    
if __name__ == "__main__":
    operation_sheet = OperationSheet()
    