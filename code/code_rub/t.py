# Số bạn muốn mã hóa
your_number = 1

# Mã hóa số thành 2 byte
encoded_bytes = your_number.to_bytes(5, byteorder='big')
print(encoded_bytes)

print(int.from_bytes(encoded_bytes, byteorder="big"))