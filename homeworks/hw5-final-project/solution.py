#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Final project solution"""

import argparse
from timeit import default_timer as timer

def main():
    # Парсим опции командной строки
    parser = argparse.ArgumentParser(description='Neural ranking homework solution')
    parser.add_argument('--submission_file', required=True, help='output Kaggle submission file')
    parser.add_argument('data_dir', help='input data directory')
    args = parser.parse_args()

    # Будем измерять время работы скрипта
    start = timer()

    # Тут вы, скорее всего, должны проинициализировать фиксированным seed'ом генератор случайных чисел для того, чтобы ваше решение было воспроизводимо.
    # Например (зависит от того, какие конкретно либы вы используете):
    #
    # random.seed(42)
    # np.random.seed(42)
    # torch.manual_seed(42)
    # transformers.set_seed(422)
    # и т.п.

    # Дальше вы должны:
    # - загрузить датасет VK MARCO из папки args.data_dir
    # - обучить свою модель с использованием train- и dev-сплитов датасета
    # - или, альтернативно, скачать и применить какую-то стороннюю модель
    # - загрузить пример сабмишна из args.data_dir/sample_submission.csv
    # - применить модель ко всем запросам и документам из примера сабмишна
    # - переранжировать документы из примера сабмишна в соответствии с предиктами вашей модели
    # - сформировать ваш сабмишн для заливки на Kaggle и сохранить его в файле args.submission_file

    # Репортим время работы скрипта
    elapsed = timer() - start
    print(f"finished, elapsed = {elapsed:.3f}")


if __name__ == "__main__":
    main()
