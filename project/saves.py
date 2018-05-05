import subprocess
import os
import re

import argparse


def save_filter(listdir):
    for file in listdir:
        res = re.match('.+-(\d+).(zip|7z)', file)
        if res is not None:
            yield int(res.group(1))

def main():
    parser = argparse.ArgumentParser(description='Архивирует указанную папку и загружает в Google Drive')
    parser.add_argument('-a', '--archiver', help='Путь к архиватору 7z')
    parser.add_argument('-n', '--arc-name', help='Имя файла архива')
    parser.add_argument('-p', '--path',     help='Путь к файлу/каталогу для архивирования', action='append',)
    # parser.add_argument('-gd', '--gdrive-dir',    help='id архива в Google Drive')
    # parser.add_argument('-gp', '--gdrive-parent', help='id родительского каталога в Google Drive')
    args = parser.parse_args()

    save_index = max(save_filter(os.listdir(path="."))) + 1
    save_name = '{}-{}'.format(args.arc_name, save_index)

    cmd = [args.archiver, 'a', save_name]
    cmd.extend(args.path)
    if subprocess.call(cmd, shell=True) != 0:
        print('Ошибка Архивирования!')
        return

    print(cmd)
    return

    arc_filename = '.'.join([args.arc_name, '7z'])
    try:
        upload(
            arc_filename,
            args.gdrive_dir,
            args.gdrive_parent,
        )
    finally:
        os.remove(arc_filename)


if __name__ == "__main__":
    main()
