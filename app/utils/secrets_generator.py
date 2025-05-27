# https://metanit.com/python/tutorial/6.9.php
import secrets
import string

characters = string.ascii_letters + string.digits
password = "".join(secrets.choice(characters) for i in range(8))

print(f"пароль из 8 символов (алфавитно-цифровых) \n{password}\n")


def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(characters) for _ in range(length))
        # Гарантируем наличие разных типов символов
        if (any(c.islower() for c in password) >= 1  # строчная буква
                and any(c.isupper() for c in password) >= 1 # заглавная буква
                and sum(c.isdigit() for c in password) >= 3  # 3 цифры
                and any(c in string.punctuation for c in password) >=1
        ):
            return password

print(f"восьмизначный буквенно-цифровой пароль, содержащий как минимум одну строчную букву, "
      f"как минимум одну заглавную букву и как минимум три цифры \n{generate_password()}\n")


# Генерация случайного числа в диапазоне
secure_number = secrets.randbelow(50)  # от 0 до 99
print(f"Генерация случайного числа в диапазоне от 0 до 99 \n{secure_number}\n")

# Применение функции secrets.randbits() для генерации числа с определенным количеством битов:
number = secrets.randbits(7)    # из 7 битов
print(f"генерация числа из 7 битов \n{number}\n")

# Если значение не указано, используется разумное значение по умолчанию
token = secrets.token_bytes()
print(f"Если значение не указано, используется разумное значение по умолчанию \n{token}\n")

# случайная строка байтов, содержащей nbytes количество байтов
token = secrets.token_bytes(10)
print(f"случайная строка байтов, содержащей nbytes количество байтов  \n{token}\n")

# Создание 16-байтового токена в шестнадцатеричном формате
token = secrets.token_hex(16)
print(f"Создание 16-байтового токена в шестнадцатеричном формате \n{token}\n")

# Создание URL-безопасного токена
url_token = secrets.token_urlsafe(16)
print(f"Создание URL-безопасного токена \n{url_token}\n")