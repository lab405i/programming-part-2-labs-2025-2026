"""
Laboratory Work 2
Network Device Availability Monitoring Using ICMP Requests

Course:
    Programming. Part 2

Topic:
    Development of a Python tool for monitoring the availability
    of a network device using ICMP ping requests.

Description:
    This program checks the availability of a network device by IP address
    or domain name. If the device is unavailable, the program simulates
    a reboot process, displays a progress bar, plays sound notifications,
    and shows a Windows message box at startup.

University:
    Kharkiv National University of Radio Electronics (NURE)

Author:
    Pavlo Galkin

Academic years:
    2025–2026

Language:
    Python 3

Required libraries:
    icmplib

Run examples:
    python ping_device_monitor.py 192.168.1.1
    python ping_device_monitor.py doed.nure.ua

Note:
    The program is designed for educational purposes as part of
    Laboratory Work 2 for the course "Programming. Part 2".
"""



from icmplib import ping
import sys
import subprocess
import socket
import time
import winsound 
import tkinter as tk
from tkinter import messagebox

PROGRAM_NAME = "Router Monitor"
PING_COUNT = 10
PING_INTERVAL = 0.5
PING_TIMEOUT = 1
REBOOT_TIME = 10


def show_start_message():
    """
    Shows a Windows pop-up message when the program starts.
    """
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo(
        PROGRAM_NAME,
        "Програма запущена. Починаємо перевірку пристрою!!!"
    )


def reboot_progress(seconds=10):
    """
    Simulates the reboot process of a network device.

    Parameters:
        seconds (int): reboot simulation duration in seconds
    """
    print("\nІмітація перезавантаження пристрою:")

    for i in range(seconds + 1):
        percent = int((i / seconds) * 100)
        filled = i
        empty = seconds - i

        bar = "█" * filled + "░" * empty

        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()

        winsound.Beep(900, 100)
        time.sleep(1)

    print("\nПристрій перезавантажено.")
    print("Живлення включено.")


def resolve_target(target):
    """
    Resolves a domain name or IP address to an IP address.

    Parameters:
        target (str): IP address or domain name

    Returns:
        str: resolved IP address
    """
    try:
        ip = socket.gethostbyname(target)
        print(f"Домен/IP: {target}")
        print(f"IP-адреса: {ip}")
        return ip
    except socket.gaierror:
        print(f"Помилка: не вдалося отримати IP-адресу для: {target}")
        sys.exit(1)


def check_device(ip):
    """
    Checks the availability of a network device using ICMP ping.

    Parameters:
        ip (str): IP address of the device

    Returns:
        object: ping result object from icmplib
    """
    print("\nВиконується перевірка доступності пристрою...")
    print(f"Кількість ICMP-запитів: {PING_COUNT}")
    print(f"Інтервал між запитами: {PING_INTERVAL} с")
    print(f"Таймаут відповіді: {PING_TIMEOUT} с\n")

    host = ping(
        ip,
        count=PING_COUNT,
        interval=PING_INTERVAL,
        timeout=PING_TIMEOUT
    )

    return host


def print_ping_statistics(host):
    """
    Prints ping statistics.

    Parameters:
        host: ping result object from icmplib
    """
    print("Результати перевірки:")
    print(f"Доступний: {host.is_alive}")
    print(f"Надіслано пакетів: {host.packets_sent}")
    print(f"Отримано пакетів: {host.packets_received}")
    print(f"Втрати пакетів: {host.packet_loss}%")
    print(f"Мінімальна затримка: {host.min_rtt} ms")
    print(f"Середня затримка: {host.avg_rtt} ms")
    print(f"Максимальна затримка: {host.max_rtt} ms")


def handle_device_status(host):
    """
    Handles the device status after ping test.
    If the device is unavailable, reboot simulation is started.

    Parameters:
        host: ping result object from icmplib
    """
    if host.is_alive:
        print("\nСтан: живлення є, мережевий пристрій доступний.")
        winsound.MessageBeep(winsound.MB_OK)
    else:
        print("\nСтан: пристрій недоступний.")
        print("Потрібно перезавантажити.")

        winsound.Beep(1000, 500)
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

        reboot_progress(REBOOT_TIME)

        messagebox.showinfo(
            PROGRAM_NAME,
            "Імітацію перезавантаження завершено. Живлення включено."
        )


def print_usage():
    """
    Prints program usage information.
    """
    print("Помилка: не вказано IP-адресу або доменне ім’я.")
    print("Приклади запуску:")
    print("python ping_test.py 192.168.1.1")
    print("python ping_test.py google.com")


def main():
    """
    Main program function.
    """
    show_start_message()

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    target = sys.argv[1]

    ip = resolve_target(target)
    host = check_device(ip)

    print_ping_statistics(host)
    handle_device_status(host)


if __name__ == "__main__":
    main()
