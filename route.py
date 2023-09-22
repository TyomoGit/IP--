"""tracerouteを自動でやるやつ"""

import subprocess
import os

# TTLの値を変更する場合はここ
TTL_COUNT = 50


def main() -> None:
    """
    各アドレスに対してtracerouteコマンドを実行し、結果を保存します。
    """

    with open("./ip_input.txt", mode="r") as f:
        ip_list = f.read().splitlines()

    try:
        os.mkdir("./traceroute_result")
    except FileExistsError:
        pass

    print("処理開始")
    print(f"***TTL(Time to Live)が{TTL_COUNT}を超える場合、それ以上は記録されません。***")

    for address in set(ip_list):
        with open(f"./traceroute_result/{address}.txt", mode="a") as f:
            process = subprocess.Popen(
                f"traceroute -m {TTL_COUNT} {address}",
                shell=True,
                stdout=f,
                stderr=f,
                text=True
            )


if __name__ == "__main__":
    main()
