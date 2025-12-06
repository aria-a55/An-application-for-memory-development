from stroop_test_ui import StroopTestUI

def start_stroop_test(main_window=None):
    test = StroopTestUI(main_window)
    test.start()

if __name__ == "__main__":
    start_stroop_test()