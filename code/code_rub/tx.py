import os

# Đường dẫn cha
parent_path = "/home/user/documents"

# Đường dẫn con
child_path = "/home/usdocuments/prect/files"

# Sử dụng os.path.join() để nối đường dẫn cha và đường dẫn con lại với nhau
full_path = os.path.relpath(child_path, parent_path)

print("Đường dẫn kết hợp:", full_path)
