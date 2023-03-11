import time
import manager

while True:
    if manager.is_connected():
        with manager.Manager("task.csv") as task:
            for site in manager.reader(task, ';'):
                result = site.check()
                print(result[0])
                checking = result[1]
                while True:
                    start_time = time.perf_counter()
                    try:
                        s = next(checking)
                    except StopIteration:
                        break
                    end_time = time.perf_counter()
                    print(
                        ' | '.join(s[:4]) +
                        ' | ' +
                        str(round((end_time - start_time) * 1000, 2)) +
                        ' ms' +
                        ' | ' +
                        ' | '.join(s[4:6])
                    )
                print()
    else:
        print("connection lost")
    print('\n\n')