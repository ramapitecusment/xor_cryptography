import binascii
from itertools import cycle


def xor(message, key):
    return bytes(log ^ a1 for log, a1 in zip(message, cycle(key)))


def un_xor(message, key):
    return bytes(log ^ a1 for log, a1 in zip(message, cycle(key)))


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def open_file():
    try:
        dic = {}
        for line in open('Cryptography.txt', "r+"):
            key, value = line.strip().split(":")
            dic[key] = value
        return dic
    except IOError:
        print("cannot open", 'the database')


def add_credentials_to_file(login_xor, password_xor):
    try:
        f = open('Cryptography.txt', "a+")
        s = "{0}:{1}".format(login_xor, password_xor) + "\n"
        print("I have been successfully registered!!!")
        f.write(s)
        f.close()
    except IOError:
        print("cannot open", 'the database')


def add_inf(login, password, dic):
    try:
        i = 0
        login_text = text_from_bits(login, encoding='utf-8')
        password_text = text_from_bits(password, encoding='utf-8')
        key = b'01010101'
        login = bytes(login, 'utf-8')
        password = bytes(password, 'utf-8')

        if 6 <= len(login_text) <= 20 and 6 <= len(password_text) <= 20:
            login_xor = str(xor(login, key)).replace("\\x0", "")[2:-1]
            password_xor = str(xor(password, key)).replace("\\x0", "")[2:-1]
            if len(dic) != 0:
                for element in dic:
                    i = i + 1
                    if login_xor == element:
                        print("This login already exists")
                        break
                    if login_xor != element and i == len(dic):
                        add_credentials_to_file(login_xor, password_xor)
            else:
                add_credentials_to_file(login_xor, password_xor)
        else:
            print("The length of the password and login must be more than 5 and less than 19!!!")

    except IOError:
        print("cannot open", 'the database')


def authorization(login, password, dic):
    are_credentials_correct = False
    key = b'01010101'
    login = bytes(login, 'utf-8')
    password = bytes(password, 'utf-8')
    login_xor = str(xor(login, key)).replace("\\x0", "")[2:-1]
    password_xor = str(xor(password, key)).replace("\\x0", "")[2:-1]
    for login_info in dic:
        if login_xor == login_info and password_xor == dic[login_info]:
            print("Successful authorization!!!!")
            are_credentials_correct = True
            break
    if not are_credentials_correct:
        print("Incorrect login or password")


def input_credentials():
    login_input = str(input("Please input the login: "))
    login_to_bits = text_to_bits(login_input, encoding='utf-8')
    password_input = str(input("Please input the password: "))
    password_to_bits = text_to_bits(password_input, encoding='utf-8')
    return login_to_bits, password_to_bits


IfReg = input("Do you have an account? Press Y if Yes and N if not! ")

if IfReg == "Y":
    login_bits, password_bits = input_credentials()
    try:
        authorization(login_bits, password_bits, open_file())
    except TypeError:
        print("The database does not exist")

elif IfReg == "N":
    IfReg = input("Do you want to create an account? Press Y if Yes and N if not! ")
    if IfReg == "Y":
        login_bits, password_bits = input_credentials()
        add_inf(login_bits, password_bits, open_file())
    else:
        print("GoodBye")
else:
    print("Please input the correct answer!!!")
