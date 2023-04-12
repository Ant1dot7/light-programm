import time
from tqdm import tqdm
import pyzipper
import rarfile
import multiprocessing as mp

rarfile.UNRAR_TOOL = r"C:\\Program Files\\WinRAR\\UnRAR.exe"


def get_list_passwords(path_to_file_passwords):
    list_pass = {}
    try:
        with open(path_to_file_passwords, 'rb') as file:
            lines = file.readlines()
    except:
        print("Файл паролей не был найден")
        return
    # Определение размера частей
    num_lines = len(lines)
    chunk_size = num_lines // 5  # Размер одной части
    remainder = num_lines % 5  # Остаток строк, которые не вошли в равные части
    # Итерация по строкам и разбиение на части
    for i, line in enumerate(lines):
        line = line.strip()  # Удаление символа перевода строки
        if i < chunk_size * 5 + min(remainder, 5):
            list_pass.setdefault(i % 5 + 1, []).append(line)
    return list_pass


def brute(password, path):
    try:
        if path.endswith('.zip'):
            with pyzipper.AESZipFile(path) as zf:
                zf.extractall(pwd=password)
        else:
            rar_file = rarfile.RarFile(path)
            rar_file.extractall(pwd=password)
        return password
    except:
        pass


def get_pass(lst, path, stop_event):
    for check_pass in tqdm(lst, total=len(lst), unit='word'):
        if stop_event.is_set():
            return
        correct_pass = brute(check_pass, path)
        if correct_pass:
            stop_event.set()
            time.sleep(2)
            print("Найден пароль:", check_pass.decode(), '\nДля завершения работы нажмите enter.')
            return correct_pass


def main():
    print(r'Если архив .rar - файл "UnRAR.exe" должен быть по пути: C:\\Program Files\\WinRAR\\UnRAR.exe!')
    path = input("Введите путь к архиву .rar или .zip: ")
    if not path.endswith('.zip') and not path.endswith('.rar'):
        print('Введите корректный путь к .rar или .zip архиву.')
        return
    path_to_file_passwords = input("Введите путь библиотеке с паролями: ")
    list_pass = get_list_passwords(path_to_file_passwords)
    if not list_pass:
        return
    stop_event = mp.Event()
    for i in range(1, 6):
        mp.Process(target=get_pass, args=(list_pass[i], path, stop_event)).start()
    input('')


if __name__ == '__main__':
    main()
