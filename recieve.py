from subprocess import Popen, PIPE

all_procs: list[Popen] = []

PACKET_LOOP_COUNT = 100
PACKET_ANALYSIS_LENGTH = 100

def main():
    rtl_fm = Popen(
        ["rtl_fm", "-f", "145.15M", "-"],
        stdout=PIPE,
    )
    all_procs.append(rtl_fm)

    direwolf = Popen([
        "direwolf", "-t", "0", "-n", "1", "-r", "24000", "-b", "16", "-q", "d",
        "-"
    ],
                     stdin=rtl_fm.stdout,
                     stdout=PIPE)

    was_lost = []
    last_id = None

    for line in direwolf.stdout:
        # print("[DW] ", line[:-1].decode())
        if b"WB2OSZ-15>TEST:XX4XXX C3 A1 D4 C3 F6 C3 F6 B2 B2 C3#" in line:
            id = int(line[-9:-7], 16)
            if last_id is None:
                last_id = id
                was_lost.append(False)
                print("First packet received")
                continue

            skipped = (id - (last_id + 1) + PACKET_LOOP_COUNT) % PACKET_LOOP_COUNT
            last_id = id
            was_lost += ([True] * skipped)
            was_lost.append(False)

            if len(was_lost) > PACKET_ANALYSIS_LENGTH:
                was_lost = was_lost[-PACKET_ANALYSIS_LENGTH:]

            mapped = "".join(map(lambda x: "_" if x else "X", was_lost))

            lost_count = was_lost.count(True)
            print(f"#{id:02d} Lost {lost_count:<3}of last {len(was_lost):<3} ({round(lost_count / len(was_lost) * 100):>2}% loss) [{mapped}]", end="\r")


def callback(x):
    print(repr(x))


if __name__ == "__main__":
    try:
        main()
    finally:
        for proc in all_procs:
            print(f"killing {proc}")
            proc.kill()
            proc.wait()
