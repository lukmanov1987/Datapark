import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

from typing import List, Optional, Dict, Union, Tuple

import pandas as pd

def plot_funnel(data: pd.DataFrame,
                stages: List[str],                
                len_data: Optional[int] = None) -> None:
    """
    Строит воронку на основе DataFrame с данными этапов.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame с данными
    stage_columns : List[str]
        Список колонок, представляющих этапы (например, ['time_offer', 'time_assign', ...])    
    len_data : Optional[int], default=None
        Общее количество заказов. Если None, берется количество строк в data """
    
   
    # Рассчитываем значения из датасета
    values = [
        len_data,                                            
        len_data - data['time_offer'].isna().sum(),      
        len_data - data['time_assign'].isna().sum(),     
        len_data - data['time_arrive'].isna().sum(),     
        len_data - data['trip_time'].isna().sum()        
    ]   
    
    
    fig = go.Figure(go.Funnel(
        y = stages,
        x = values,
        textposition = "inside",
        textinfo = "value+percent initial",
        marker = {"color": px.colors.sequential.Blues_r},
        orientation = "h",
        hovertemplate = "<b>%{y}</b><br>" +
                       "Количество: %{x:,}<br>" +
                       "Конверсия от предыдущего этапа: %{percentPrevious:.1%}<br>" +
                       "<extra></extra>",
        texttemplate = "%{value:,}<br>%{percentInitial:.1%}"
    ))
    
    
    fig.update_layout(
        title = "Воронка заказов такси",
        title_x = 0.5,  # Простое выравнивание по центру
        font = {"size": 12},
        height = 500
    )
    
    fig.show() 


def compare_funnel_groups(control_group: pd.DataFrame, test_group: pd.DataFrame, stages: List[str]) -> None:
    """
    Строит воронки конверсии для двух групп.
    
    Parameters
    ----------
    control_group : pd.DataFrame
        DataFrame контрольной группы с колонками этапов
    test_group : pd.DataFrame
        DataFrame тестовой группы с колонками этапов
    stages : List[str]
        Список названий этапов воронки (соответствуют колонкам DataFrame)
    
    Returns
    -------
    None
        Отображает интерактивный график с двумя воронками и аннотациями этапов. """
    # Рассчитываем воронку для группы A
    values_control = [
        len(control_group),
        len(control_group) - control_group['time_offer'].isna().sum(),
        len(control_group) - control_group['time_assign'].isna().sum(),
        len(control_group) - control_group['time_arrive'].isna().sum(),
        len(control_group) - control_group['trip_time'].isna().sum()
    ]
    
    # Рассчитываем воронку для группы B
    values_test = [
        len(test_group),
        len(test_group) - test_group['time_offer'].isna().sum(),
        len(test_group) - test_group['time_assign'].isna().sum(),
        len(test_group) - test_group['time_arrive'].isna().sum(),
        len(test_group) - test_group['trip_time'].isna().sum()
    ]
    
       
    # Создаем субплоты с двумя воронками
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Контрольная группа', 'Тестовая группа'),
        specs=[[{"type": "funnel"}, {"type": "funnel"}]],
        horizontal_spacing=0.20  # Увеличиваем расстояние между графиками
    )
    
    # Добавляем воронку для контрольной группы  без подписей этапов
    fig.add_trace(go.Funnel(
        name='Контрольная группа',
        y=stages,
        x=values_control,
        marker=dict(
            color='#1f77b4',
            line=dict(color='#1f77b4', width=2)
        ),
        textinfo="value+percent initial",    
        showlegend=False,
        hoverinfo = 'none'        
    ), 1, 1)
    
    # Добавляем воронку для тестовой группы без подписей этапов
    fig.add_trace(go.Funnel(
        name='Те', 
        y=stages,
        x=values_test,
        marker=dict(
            color='#ff7f0e',
            line=dict(color='#ff7f0e', width=2)
        ),
        textinfo="value+percent initial",    
        showlegend=False,
        hoverinfo = 'none'        
    ), 1, 2)
    
    # Добавляем аннотации с названиями этапов между графиками
    for i, stage in enumerate(stages):
        fig.add_annotation(
            x=0.5, 
            y=1 - (i + 0.5) / len(stages),  # Равномерное распределение по вертикали
            xref="paper",
            yref="paper",
            text=stage,
            showarrow=False,
            font=dict(size=12),
            xanchor="center"
        )
    
    fig.update_layout(
        title_text="Сравнение воронок по тестовым группам",
        title_x=0.5,
        height=500,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    # Убираем подписи этапов у обеих воронок
    fig.update_yaxes(showticklabels=False, row=1, col=1)
    fig.update_yaxes(showticklabels=False, row=1, col=2)
    
    fig.show()


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