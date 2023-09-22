"""whois解析を自動でやるやつ"""
import subprocess
import re
import os

import route

TMP_FILE = "./__whois_tmp.txt"


def shape(path: str, keyword: str) -> list[str]:
    """
    whoisの結果を整形する関数です。
    """
    with open(str(path), mode="r") as f:
        result = f.read()
    result = re.sub(r" +", " ", result)
    lines = result.splitlines()
    descrs = []
    for line in lines:
        if "descr:" in line:
            descrs.append(line)
    return [" ".join(descr.split(" ")[1:]) for descr in descrs]


def shape_whois_result_apnic(path: str) -> list[str]:
    with open(str(path), mode="r") as f:
        result = f.read()
    result = re.sub(r" +", " ", result)
    lines = result.splitlines()
    descrs = []
    for line in lines:
        if "descr:" in line:
            descrs.append(line)
    return [" ".join(descr.split(" ")[1:]) for descr in descrs]


def shape_whois_result_jpnic(path: str) -> list[str]:
    with open(str(path), mode="r") as f:
        result = f.read()
    result = re.sub(r" +", " ", result)
    lines = result.splitlines()
    organizations = []
    for line in lines:
        if "[Organization]" in line:
            organizations.append(line)
    return [" ".join(org.split(" ")[2:]) for org in organizations]

# def shape_whois_result(path: str, nic_type: str = "jpnic") -> str:
#     """
#     whoisの結果から組織情報だけを抽出し、それを返します。
#     ----
#     path: whoisの結果が書かれたファイルのパス
#     """
#     with open(str(path), mode="r") as f:
#         result = f.read()
#     result = re.sub(r" +", " ", result)
#     lines = result.splitlines()
#     for line in lines:
#         if nic_type == "jpnic":
#             if "[Organization]" in line:
#                 return " ".join(line.split(" ")[2:])
#         elif nic_type == "apnic":
#             if "descr:" in line:
#                 return " ".join(line.split(" ")[1:])
#     print("!!!", result)
#     return "None"


def run_whois(line: str) -> str:
    """
    tracerouteをした結果の一行に対してwhoisを実行します。
    ----
    line: tracerouteの結果の一行
    nic: whoisサーバーのアドレス
    """
    line = line.replace("(", "").replace(")", "")
    blocks = line.split(" ")
    whois_result = []

    for block in blocks:
        if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", block):

            with open(TMP_FILE, mode="w") as f:
                _ = subprocess.run(
                    f"whois -h whois.apnic.net {block}", shell=True, stdout=f, stderr=f, text=True
                )
                whois_result = shape_whois_result_apnic(TMP_FILE)

            # APNICで検索できない場合はJPNICを参照する
            if whois_result == ["Japan Network Information Center"]:
                with open(TMP_FILE, mode="w") as f:
                    _ = subprocess.run(
                        f"whois -h whois.nic.ad.jp {block}/e", shell=True, stdout=f, stderr=f, text=True
                    )
                    whois_result = shape_whois_result_jpnic(TMP_FILE)
            break

    if whois_result == []:
        return line + "【whois】None"
    for i, element in enumerate(whois_result):
        line += f"【whois{i}】{element}\n"
    return line


def main() -> None:
    """
    各アドレスに対してwhoisコマンドを実行し、結果を保存します。
    """
    with open("./ip_input.txt", mode="r") as f:
        ip_list = f.read().splitlines()
        
    try:
        os.mkdir("./whois_result")
    except FileExistsError:
        pass

    print("処理開始")
    ip_set = set(ip_list)
    for i, address in enumerate(ip_set):
        print("処理中", address, f"({i+1}/{len(ip_set)}件)")
        with open(f"./traceroute_result/{address}.txt") as f:
            lines = f.readlines()

        result = lines[0] + "\n"
        for line in lines[1:]:
            whois_result = run_whois(line)
            result += whois_result + "\n"

        with open(f"./whois_result/{address}.txt", mode="w") as f:
            f.write(result)

    os.remove(TMP_FILE)


if __name__ == "__main__":
    main()
