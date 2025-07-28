from celery import shared_task
from utils.database_requests import get_all_objects_from_model
from .models import User


def assign_rank_to_users(users, start_index, count, rank_name):
    """Присваивает указанный ранг заданному количеству пользователей"""
    end_index = start_index + count
    for i in range(start_index, min(end_index, len(users))):
        users[i].rank = rank_name
    return end_index


def distribute_remaining_users(users, start_index, rank_groups):
    """Распределяет пользователей по группам рангов"""
    current_index = start_index
    total_users = len(users) - start_index
    group_size = total_users // len(rank_groups)
    remainder = total_users % len(rank_groups)

    for rank_name in rank_groups:
        count = group_size + (1 if remainder > 0 else 0)
        current_index = assign_rank_to_users(users, current_index, count, rank_name)
        remainder -= 1 if remainder > 0 else 0
    return current_index


def calculate_user_ranks(users):
    """Основная функция для расчета рангов пользователей"""
    if not users:
        return []
    top_ranks = ["Легенда", "Элита", "Мастер"]
    for i in range(min(3, len(users))):
        users[i].rank = top_ranks[i]

    # Распределение остальных пользователей
    rank_groups = [
        "gold 3",
        "gold 2",
        "gold 1",
        "silver 3",
        "silver 2",
        "silver 1",
        "bronze 3",
        "bronze 2",
        "bronze 1",
    ]

    current_index = 3  # Начинаем после топ-3
    current_index = distribute_remaining_users(users, current_index, rank_groups)

    # Все оставшиеся получают bronze 1
    assign_rank_to_users(users, current_index, len(users) - current_index, "bronze 1")

    return users


@shared_task
def daily_refresh():
    users = get_all_objects_from_model(User)
    sorted_users = sorted(users, key=lambda x: (-x.stars, x.last_update))
    users = calculate_user_ranks(sorted_users)
    for user in users:
        user.energy = 500
        user.save()
    return "Задача выполнена: Ранги и энергия обновились!"
