import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from typing import List, Optional, Dict, Union

def analyze_group_period(data_group: pd.DataFrame, group_labels: str = "") -> None:
    """
    Анализирует и выводит временной период для группы.

    Parameters
    ----------
        data_group: строка DataFrame (Series) с временными метками.
        group_labels: строка с бинарной метрикой группы.
       
    Returns
    -------
    None
        Функция выводит результаты анализа в консоль, но ничего не возвращает
    """
    min_date = data_group['time_order'].min()
    max_date = data_group['time_order'].max()
    time_lapse = max_date - min_date   
    

    print(f" {group_labels}")
    print(f" Начало периода: {min_date}")
    print(f" Конец периода:  {max_date}")
    print(f" Общая продолжительность: {time_lapse}")   



def calc_time_diff(df: pd.DataFrame, start_col: str, end_col: str) -> Union[pd.Series, float]:
    """Рассчитывает разницу во времени между двумя столбцами в секундах.
    
    Parameters
    ----------
        df: Строка DataFrame (Series) с временными метками.
        start_col: Название столбца с начальным временем.
        end_col: Название столбца с конечным временем.
    
    Returns:
        float: Разница в секундах или NaN, если хотя бы одна из меток отсутствует.
    """
    if pd.isna(df[start_col]) or pd.isna(df[end_col]):
        return np.nan
    return (df[end_col] - df[start_col]).total_seconds()

def analyze_metrics(df_control: pd.DataFrame, df_test: pd.DataFrame, column_name: str, alpha=0.05) -> None:

    """
    Проводит статистический анализ бинарной метрики для контрольной и тестовой групп.
    
    Функция выполняет анализ конверсии (бинарной метрики) между двумя группами:
    - рассчитывает конверсию, абсолютную и относительную разницу
    - проводит Z-тест для пропорций
    - выводит вывод о статистической значимости различий
    
    Parameters
    ----------
    df_control : pd.DataFrame
        DataFrame с данными контрольной группы (группа A).
        Должен содержать колонку с бинарной метрикой.
    df_test : pd.DataFrame
        DataFrame с данными тестовой группы (группа B).
        Должен содержать колонку с бинарной метрикой.
    column_name : str
        Название колонки с бинарной метрикой
        
    alpha : float, default=0.05
        Уровень значимости для статистических тестов.
        Используется для определения порога p-value.
    
    Returns
    -------
    None
        Функция выводит результаты анализа в консоль, но ничего не возвращает.
        
    Функция выполняет следующие расчеты:
        1. Конверсия = среднее значение бинарной метрики
        2. Абсолютная разница = conv_B - conv_A
        3. Относительная разница = (conv_B / conv_A - 1) * 100%
        4. Z-тест для пропорций (двусторонний)"""
    
     
    print("="*60)
    print(f"АНАЛИЗ ЭТАПА {column_name[3:]}")
    print("="*60)
    
    # 1. АНАЛИЗ КОНВЕРСИИ (бинарная метрика)
    
    conv_a = df_control[column_name].mean()
    conv_b = df_test[column_name].mean()
    print(f"   Группа A: {conv_a:.4f} ({df_control[column_name].sum()}/{len(df_control)})")
    print(f"   Группа B: {conv_b:.4f} ({df_test[column_name].sum()}/{len(df_test)})")
    print(f"   Абсолютная разница: {conv_b - conv_a:.4f}")
    print(f"   Относительная разница: {(conv_b/conv_a - 1)*100:.2f}%")
    
    # Z-тест для пропорций
    count = [df_control[column_name].sum(), df_test[column_name].sum()]
    nobs = [len(df_control), len(df_test)]
    zstat, p_value_conv = proportions_ztest(count, nobs, alternative='two-sided')
    print(f"   Z-тест: p-value = {p_value_conv:.5f}")
    
    if p_value_conv < alpha:
        print(f"   ✅ Статистически значимая разница в конверсии!")
    else:
        print(f"   ❌ Нет значимой разницы в конверсии") 