https://fair-snowplow-f68.notion.site/Final-Project-acd24a76f5ef4a50b2d86f3e7d47afd3

The templates Table of Variables.
```py
self.current_user = None || ""
self.users = [
    {"username": "", "account": "", "password": ""}
] 
self.sheets = [{
    "owner_name": "",
    "sheet_name": "",
    "user_list": [{
        "user_name": "",
        "access_right": ReadOnly || WriteOnly || ReadWrite
    }],
    "content": []
}] 
```