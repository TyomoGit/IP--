import subprocess
import os
import route


def main() -> None:
    with open("./ip_input.txt", mode="r") as f:
        ip_list = f.read().splitlines()
    
    PING_COUNT = 5
    ip_set = set(ip_list)
    try:
        os.mkdir("./ping_result")
    except FileExistsError:
        pass

    for address in ip_set:
        with open(f"./ping_result/{address}.txt", mode="w") as f:
            process = subprocess.Popen(
                f"ping -c {PING_COUNT} {address}",
                shell=True,
                stdout=f,
                stderr=f,
                text=True
            )


if __name__ == "__main__":
    main()
