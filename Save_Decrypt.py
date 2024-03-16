import chardet
from Crypto.Cipher import AES
import base64

global key
key = "tiencikpncoanvsnauewjxzogtrdfkes".encode('utf-8')

# 文件编码检测
def get_encoding(file):
    with open(file,'rb') as f:
        tmp = chardet.detect(f.read())
        return tmp['encoding']

def unpad(s):
    last_num = s[-1]
    text = s[:-last_num]
    return text

def pad(data):
    text = data + chr(16 - len(data) % 16) * (16 - len(data) % 16)
    return text

def aes_ECB_Decrypt(data):   # ECB模式的解密函数，data为密文，key为16字节密钥
    # key = key.encode('utf-8')
    aes = AES.new(key=key,mode=AES.MODE_ECB)  # 创建解密对象
 
    #decrypt AES解密  B64decode为base64 转码
    result = aes.decrypt(base64.b64decode(data))
    result = unpad(result)            # 除去补16字节的多余字符
    return str(result,'utf-8')        # 以字符串的形式返回

def aes_ECB_Encrypt(data):   # ECB模式的加密函数，data为明文，key为16字节密钥
    data = pad(data)             # 补位
    data = data.encode('utf-8')
    aes = AES.new(key=key,mode=AES.MODE_ECB)  #创建加密对象
    #encrypt AES加密  B64encode为base64转二进制编码
    result = base64.b64encode(aes.encrypt(data))
    return str(result,'utf-8')        # 以字符串的形式返回


def read_Origin(filepath,encoding):
    with open(filepath,mode='r',encoding=encoding) as f : 
        data = f.read()
        f.close()
        return data

def save_DecryptJson(filepath,data):
    with open(filepath + ".json" ,mode="w",encoding="utf8") as f :
        f.write(data)

def save_Archive(filepath,data):
    with open(filepath + "_1" ,mode="w",encoding="ascii") as f :
        f.write(data)        




if __name__ == '__main__':
    filepath = ""
    filepath = input("请输入文件路径:")
    encoding = get_encoding(filepath)
    print("FileEncoding: " + encoding)
    p = input("输入“1” 解密文件，输入“2”加密文件\n 解密后文件名将保存为同名的json文件\n 加密只需输入原存档路径即可\n 加密后存档名称后会加“_1”，导入时记得删除\n")
    if p == "1":
        DecryptData = aes_ECB_Decrypt(read_Origin(filepath,encoding))
        save_DecryptJson(filepath,DecryptData)
        print("解密成功")

    if p == "2":
        data = read_Origin(filepath +".json",encoding)
        save_Archive(filepath,aes_ECB_Encrypt(data))
        print("加密成功 ")


        


