import base64
import hashlib
import os
import sys

# txt 格式: <固定长度魔数（暂定6位）><文件md5编码（32位）><文件全名（包括格式）base64编码>@<文件base64编码>

# file -> txt

def file_to_base64(file_path):
    with open(file_path, 'rb') as f:
        binary_data = f.read()
        text_data = base64.b64encode(binary_data).decode('utf-8')
        return text_data

def encode_base64(str):
    return base64.b64encode(str.encode('utf-8')).decode('utf-8')

def to_text(file_md5, file_full_name, file_data, magic_number='114514'):
    return magic_number + file_md5 + file_full_name + '@' + file_data

def write_temp_txt_file(text_data, temp_file):
    with open(temp_file, 'w') as f:
        f.write(text_data)

# txt -> file

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def check_magic_number(head, magic_number='114514'):
    assert head[:6] == magic_number, "魔数错误"

def get_head_md5(head):
    return head[6:38]

def decode_base64(base64_str):
    return base64.b64decode(base64_str.encode('utf-8')).decode('utf-8')

def get_real_file_name(head):
    file_base64_name = head[38:]
    file_name = decode_base64(file_base64_name)
    return file_name

def write_file(text_data, file_path):
    binary_data = base64.b64decode(text_data)
    with open(file_path, 'wb') as f:
        f.write(binary_data)

def check_file_md5(expect_md5, real_md5):
    assert expect_md5 == real_md5, "文件md5不一致，请重新操作"

def get_file_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

# main

method_type = sys.argv[1]
if method_type == '1':
    source_file = sys.argv[2]
    print("source_file: " + source_file)
    file_name_base64 = encode_base64(os.path.basename(source_file))
    print("file_name_base64: "+ file_name_base64)
    file_md5 = get_file_md5(source_file)
    print("file_md5: ", file_md5)
    file_data = file_to_base64(source_file)
    text = to_text(file_md5, file_name_base64, file_data)
    temp_file = file_md5 + '.txt'
    write_temp_txt_file(text, temp_file)
    print("生成临时文本文件: " + temp_file)
elif method_type == '2':
    temp_file_path = sys.argv[2]
    full_text = read_file(temp_file_path)
    head = full_text.split("@")[0]
    check_magic_number(head)
    real_file_name = get_real_file_name(head)
    body = full_text.split("@")[1]
    write_file(body, real_file_name)
    check_file_md5(get_head_md5(head), get_file_md5(real_file_name))
    print("已还原文件: "+ real_file_name)
else:
    print("method_type error")
