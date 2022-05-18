#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
qcc 请求头生成
"""
from ast import If
import hashlib
import hmac
import json
from urllib import parse


class SignTool(object):

    def __init__(self):
        self.seeds = {
            "0": "W",
            "1": "l",
            "2": "k",
            "3": "B",
            "4": "Q",
            "5": "g",
            "6": "f",
            "7": "i",
            "8": "i",
            "9": "r",
            "10": "v",
            "11": "6",
            "12": "A",
            "13": "K",
            "14": "N",
            "15": "k",
            "16": "4",
            "17": "L",
            "18": "1",
            "19": "8"
        }
        self.n = 20

    def generate_map_result(self, s):
        if not s:
            s = "/"
        s = s.lower()
        s = s + s
        k = ''
        for i in s:
            k += self.seeds[str(ord(i) % 20)]
        return k

    @staticmethod
    def sign_with_hmac(key, s):
        return hmac.new(bytes(key, encoding='utf-8'), bytes(s,
                                                            encoding='utf-8'),
                        hashlib.sha512).hexdigest()

    def get_head_key(self, s):
        s = s.lower()
        map_result = self.generate_map_result(s)
        key = self.sign_with_hmac(map_result, s)
        return key[10:10 + 20]

    def get_head_value(self, url, data=None):
        if not url:
            url = "/"
        if not data:
            data = {}
        key = url.lower()
        # JSON.stringify(data).toLowerCase()
        data_s = json.dumps(data, ensure_ascii=False).lower().replace(" ", "")
        enc_data = key + key + data_s
        enc_key = self.generate_map_result(key)
        result = self.sign_with_hmac(enc_key, enc_data)
        return result

    def get_header(self, url, data=None):
        paths = parse.urlparse(url)
        uri = paths.path

        if not data and len(paths.query) > 0:
            uri = paths.path + "?" + paths.query

        header_key = self.get_head_key(uri)
        header_val = self.get_head_value(uri, data)

        return {header_key: header_val}


sign_tool = SignTool()

if __name__ == '__main__':

    print("Get")
    # 5f981b0d87c5cf7281b3: 53ea71e263806f8a946c21a76b1ae632d9da6fd74818e2aa09d6e356ceba78d54c6cb220cd5c3700792e94ae58ee1caff9551dffa10c67069258bec0ba0d50fc
    print(
        sign_tool.get_header(
            "https://www.qcc.com/api/userSearch/getFilterList"))

    print("Get带参")
    # 4c897399139555b71bf5: e32def53d68b1961f844dea78c305e431765fb8adf0bced437199228efb17ceab5db330dc0bc3a6d4b67c15452610ddd60f09cad3c798c04a61876bd7bbda5df
    print(
        sign_tool.get_header(
            "https://www.qcc.com/api/sns/getGlossaryInfo?ids=26%2C27%2C58%2C28%2C30"
        ))

    print("Post")
    # db71892327c6512212ed: 3475a0488376c2ad56ab34564ed7b87676650d6ee41a9001ae0392f1847321ec7cb5560149909131388654a8706e51a6a29b659b3c94fcfa95c7952f63dcaa89
    print(
        sign_tool.get_header(
            'https://www.qcc.com/api/user/getUserCompanyInfo', {
                "keynos": [
                    "55c8f4f96d06867be1020a34bd67495f",
                    "0882d28ba58dabeb50e82c201875f9ff",
                    "2c0de807aa3e949348eeb024e347c94e",
                    "da778bec1f2c95659786149e0c40aae0",
                    "363052a0476431801838e8c2f4aff898",
                    "362513c1a18c6ac8510437f773589b4f",
                    "53563afe2e2fad6854fda6fbff1813d1",
                    "fe6979595aad38fd1efea801184e247b",
                    "00dd37659742022e637464a4a9e24b3b",
                    "7d0f54d6ccc6558ebf43ff7b6ed11d53",
                    "1216cbda8aad152cd23e14015eef605c",
                    "a2ae8e3361166e1c983ff941e7bc5b0f",
                    "f3d88c8f6ab4f27bc181dc4193685171",
                    "92ff9062d6af2715b5abc8ecf08533f2",
                    "b4c5cadf59e272b7bb033e058c196576",
                    "c8ca01663519a72d688e20b24fb6026e",
                    "c24330b8e086b40e95b8547508172394",
                    "de229319113dddcbfdad00464ffb6149",
                    "bdfc3a0936003766c00ef7b510f50795",
                    "3251a58f9bada226fd6bf36c6a524c70"
                ]
            }))
