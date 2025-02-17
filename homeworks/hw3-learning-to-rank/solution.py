#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Learning to Rank homework solution"""

import argparse
from timeit import default_timer as timer

def main():
    # Парсим опции командной строки
    parser = argparse.ArgumentParser(description='Learning to Rank homework solution')
    parser.add_argument('--train', action='store_true', help='run script in model training mode')
    parser.add_argument('--model_file', help='output ranking model file')
    parser.add_argument('--submission_file', help='output Kaggle submission file')
    parser.add_argument('data_dir', help='input data directory')
    args = parser.parse_args()

    # Будем измерять время работы скрипта
    start = timer()

    # Тут вы, скорее всего, должны проинициализировать фиксированным seed'ом генератор случайных чисел для того, чтобы ваше решение было воспроизводимо.
    # Например (зависит от того, какие конкретно либы вы используете):
    #
    # random.seed(42)
    # np.random.seed(42)
    # и т.п.

    # Какой у нас режим: обучения модели или генерации сабмишна?
    if args.train:
        # Тут вы должны:
        # - загрузить датасет VKLR из папки args.data_dir
        # - обучить модель с использованием train- и dev-сплитов датасета
        # - при необходимости, подобрать гиперпараметры
        # - сохранить обученную модель в файле args.model_file
        pass
    else:
        # Тут вы должны:
        # - загрузить тестовую часть датасета VKLR из папки args.data_dir
        # - загрузить модель из файла args.model_file
        # - применить модель ко всем запросам и документам из test.txt
        # - переранжировать документы по каждому из запросов так, чтобы более релевантные шли сначала
        # - сформировать ваш сабмишн для заливки на Kaggle и сохранить его в файле args.submission_file
        pass

    # Репортим время работы скрипта
    elapsed = timer() - start
    print(f"finished, elapsed = {elapsed:.3f}")


if __name__ == "__main__":
    main()
