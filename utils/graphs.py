import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from typing import List, Optional, Dict, Union, Tuple

def plot_funnel(data: pd.DataFrame,
                stages: List[str],                
                len_data: Optional[int] = None) -> None:
    """
    Строит классическую воронку на основе DataFrame с данными этапов (от заказа поездки наверху воронки до доставки клиента внизу). В скобках указана конверсия     к orders. Так же в области со стрелкой указана конверсия между этапами 
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame с данными
    stages : List[str]
        Список названий этапов. Инициируется в main перед запуском функции    
    len_data : Optional[int], default=None
        Общее количество заказов. Если None, берется количество строк в data
    Returns
    -------
    None
        Отображает график воронки и аннотациями ее этапов.
    """
    
    # Рассчитываем значения
    if len_data is None:
        len_data = len(data)
    
    values = [
        len_data,                                            
        len_data - data['time_offer'].isna().sum(),      
        len_data - data['time_assign'].isna().sum(),     
        len_data - data['time_arrive'].isna().sum(),     
        len_data - data['trip_time'].isna().sum()        
    ]
    
    # Переворачиваем для отрисовки сверху вниз
    stages_reversed = stages[::-1]
    values_reversed = values[::-1]
    
    # Сохраняем первое значение (orders) для расчета процентов
    first_value = values[0]  # ← ключевое изменение
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    max_value = max(values_reversed)
    n_stages = len(stages_reversed)
    
    # Рисуем сверху вниз
    for i, (stage, value) in enumerate(zip(stages_reversed, values_reversed)):
        # Ширина пропорциональна значению
        width = value / max_value
        left = (1 - width) / 2

        color_intensity = 0.3 + 0.5 * (i / n_stages)
        
        ax.barh(i, width, left=left, height=0.6,
                color=plt.cm.Blues(color_intensity),
                edgecolor='white', linewidth=2)
        
        # Текст с количеством и процентом от ПЕРВОГО этапа
        percent_initial = (value / first_value) * 100  # ← используем first_value
        ax.text(0.5, i, f'{value:,.0f}\n({percent_initial:.1f}%)',
               ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Название этапа слева
        ax.text(-0.02, i, stage, ha='right', va='center', fontsize=11,
               transform=ax.get_yaxis_transform())
        
        # Процент потерь между этапами
        if i < n_stages - 1:
            loss = (1 - values_reversed[i+1] / value) * 100
            y_pos_arrow = i + 0.5
            ax.annotate(f'↓ {loss:.1f}%', 
                   xy=(0.5, y_pos_arrow), 
                   ha='center', va='center',
                   fontsize=9, style='italic',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.7))
    
    # Настройка осей
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, n_stages - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Заголовок
    ax.set_title('Воронка заказов такси\n(от заказа до завершения поездки)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Убираем рамки
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    plt.show()
       
def compare_funnel_groups(control_group: pd.DataFrame, 
                          test_group: pd.DataFrame, 
                          stages: List[str]) -> None:
    """
    Строит воронки конверсии для двух групп (контрольная и тестовая) в стиле matplotlib.
    
    Parameters
    ----------
    control_group : pd.DataFrame
        DataFrame контрольной группы с колонками этапов
    test_group : pd.DataFrame
        DataFrame тестовой группы с колонками этапов
    stages : List[str]
        Список названий этапов воронки
    
    Returns
    -------
    None
        Отображает график с двумя воронками и аннотациями этапов между ними.
    """
    
    # Рассчитываем воронку для контрольной группы
    values_control = [
        len(control_group),
        len(control_group) - control_group['time_offer'].isna().sum(),
        len(control_group) - control_group['time_assign'].isna().sum(),
        len(control_group) - control_group['time_arrive'].isna().sum(),
        len(control_group) - control_group['trip_time'].isna().sum()
    ]
    
    # Рассчитываем воронку для тестовой группы
    values_test = [
        len(test_group),
        len(test_group) - test_group['time_offer'].isna().sum(),
        len(test_group) - test_group['time_assign'].isna().sum(),
        len(test_group) - test_group['time_arrive'].isna().sum(),
        len(test_group) - test_group['trip_time'].isna().sum()
    ]
    
    # Переворачиваем данные для отрисовки сверху вниз
    stages_reversed = stages[::-1]
    values_control_reversed = values_control[::-1]
    values_test_reversed = values_test[::-1]
    
    # Сохраняем первое значение (orders) для расчета процентов
    first_value_control = values_control[0]
    first_value_test = values_test[0]
    
    # Создаем фигуру с двумя сабплотами
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    max_value = max(max(values_control_reversed), max(values_test_reversed))
    n_stages = len(stages_reversed)
    
    # Рисуем воронку для контрольной группы (слева) с градиентом
    for i, (stage, value) in enumerate(zip(stages_reversed, values_control_reversed)):
        width = value / max_value
        left = (1 - width) / 2
        
        # Градиент: сверху (i=0) темнее, снизу (i=n_stages-1) светлее
        color_intensity = 0.3 + 0.5 * (i / n_stages)
        
        ax1.barh(i, width, left=left, height=0.6,
                color=plt.cm.Blues(color_intensity),
                edgecolor='white', linewidth=2)
        
        percent_initial = (value / first_value_control) * 100
        ax1.text(0.5, i, f'{value:,.0f}\n({percent_initial:.1f}%)',
                ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Процент потерь между этапами
        if i < n_stages - 1:
            loss = (1 - values_control_reversed[i+1] / value) * 100
            y_pos_arrow = i + 0.5
            ax1.annotate(f'↓ {loss:.1f}%', 
                        xy=(0.5, y_pos_arrow), 
                        ha='center', va='center',
                        fontsize=8, style='italic',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.7))
    
    # Рисуем воронку для тестовой группы (справа) с градиентом
    for i, (stage, value) in enumerate(zip(stages_reversed, values_test_reversed)):
        width = value / max_value
        left = (1 - width) / 2
        
        # Градиент: сверху (i=0) темнее, снизу (i=n_stages-1) светлее
        color_intensity = 0.3 + 0.5 * (i / n_stages)
        
        ax2.barh(i, width, left=left, height=0.6,
                color=plt.cm.Oranges(color_intensity),
                edgecolor='white', linewidth=2)
        
        percent_initial = (value / first_value_test) * 100
        ax2.text(0.5, i, f'{value:,.0f}\n({percent_initial:.1f}%)',
                ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Процент потерь между этапами
        if i < n_stages - 1:
            loss = (1 - values_test_reversed[i+1] / value) * 100
            y_pos_arrow = i + 0.5
            ax2.annotate(f'↓ {loss:.1f}%', 
                        xy=(0.5, y_pos_arrow), 
                        ha='center', va='center',
                        fontsize=8, style='italic',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.7))
    
    # Настройка осей для обоих графиков (убираем все шкалы)
    for ax in [ax1, ax2]:
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, n_stages - 0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        for spine in ax.spines.values():
            spine.set_visible(False)
    
    # Добавляем названия этапов между графиками с помощью fig.text
    for i, stage in enumerate(stages):
        y_pos = 0.82 - (i * 0.16)
        
        fig.text(0.5, y_pos, stage, 
                ha='center', va='center', 
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='gray', alpha=0.8))
    
    # Заголовки для групп
    ax1.set_title('Контрольная группа', fontsize=12, fontweight='bold', pad=15)
    ax2.set_title('Тестовая группа', fontsize=12, fontweight='bold', pad=15)
    
    # Общий заголовок
    fig.suptitle('Сравнение воронок по тестовым группам\n(от заказа до завершения поездки)', 
                fontsize=14, fontweight='bold', y=1.02)
    
    # Используем subplots_adjust вместо tight_layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.25)
    plt.show()



def daily_distribution_balance(daily_split: pd.DataFrame) -> None:
    """
    Строит баланс распределения по дням
    
    Parameters:
    -----------
    daily_split : pd.DataFrame
        DataFrame с временным индексом и столбцами групп для визуализации
    
    Returns:
    --------
    None
        Отображает интерактивный график c распределением групп"""
    
    plt.figure(figsize=(12, 6))
    daily_split.plot(kind='area', alpha=0.5)
    plt.title('Баланс распределения по дням')
    plt.xlabel('Дата')
    plt.ylabel('Доля группы')
    plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5)
    
    # Поворачиваем подписи дат
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() 
    plt.show()


def hourly_distribution_balance(hourly_balance: pd.DataFrame) -> None:   
    """
    Строит баланс распределения групп по часам дня.
    
    Parameters
    ----------
    hourly_balance : pd.DataFrame
        DataFrame с распределением групп по часам.
        Индекс должен содержать часы (0-23), столбцы - названия групп.
    
    Returns
    -------
    None
        Отображает столбчатый график с распределением групп по часам.
    """
    
    fig, ax = plt.subplots(figsize=(14, 6))
    hourly_balance.plot(kind='bar', ax=ax)
    ax.set_title('Баланс групп по часам дня')
    ax.set_xlabel('Час дня')
    ax.set_ylabel('Доля группы')
    ax.legend(title='Test Group')
    plt.show()