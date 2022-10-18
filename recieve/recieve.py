from subprocess import DEVNULL, Popen, PIPE
from time import sleep
from kiss import TCPKISS

all_procs: list[Popen] = []

PACKET_LOOP_COUNT = 100
PACKET_ANALYSIS_LENGTH = 100


def main():
    rtl_fm = Popen(
        ["rtl_fm", "-f", "145.00M", "-"],
        stdout=PIPE,
    )
    all_procs.append(rtl_fm)

    direwolf = Popen([
        "direwolf", "-t", "0", "-n", "1", "-r", "24000", "-b", "16", "-q", "d"
    ],
                     stdin=rtl_fm.stdout,
                     stdout=DEVNULL)

    sleep(5)  # Wait for direwolf to start

    k = TCPKISS("127.0.0.1", 8001)
    k.start()
    k.read(callback=callback)


was_lost = []
last_id = None


def callback(packet: bytes):
    global was_lost, last_id


    id = int(packet[-3:-1], 16)
    if last_id is None:
        print("First packet received")
        last_id = id
        return

    skipped = (id -
                (last_id + 1) + PACKET_LOOP_COUNT) % PACKET_LOOP_COUNT
    last_id = id
    was_lost += ([True] * skipped)
    was_lost.append(False)

    if len(was_lost) > PACKET_ANALYSIS_LENGTH:
        was_lost = was_lost[-PACKET_ANALYSIS_LENGTH:]

    mapped = "".join(map(lambda x: "_" if x else "X", was_lost))

    lost_count = was_lost.count(True)
    print(
        f"#{id:02d} Lost {lost_count:<3}of last {len(was_lost):<3} ({round(lost_count / len(was_lost) * 100):>2}% loss) [{mapped}]",
        end="\r")


if __name__ == "__main__":
    try:
        main()
    finally:
        for proc in all_procs:
            print(f"killing {proc}")
            proc.kill()
            proc.wait()
