users = [
    {"id": 1, "stars": 150, "rank": "bronze3"},
    {"id": 2, "stars": 120, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 4, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
    {"id": 3, "stars": 100, "rank": "bronze3"},
]
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
    
    
    # Топ-3 пользователя получают особые ранги
    top_ranks = ['Легенда', 'Элита', 'Мастер']
    for i in range(min(3, len(users))):
        users[i].rank = top_ranks[i]
    
    # Распределение остальных пользователей
    rank_groups = [
        'gold 3', 'gold 2', 'gold 1',
        'silver 3', 'silver 2', 'silver 1',
        'bronze 3', 'bronze 2', 'bronze 1'
    ]
    
    current_index = 3  # Начинаем после топ-3
    current_index = distribute_remaining_users(users, current_index, rank_groups)
    
    # Все оставшиеся получают bronze 1
    assign_rank_to_users(users, current_index, len(users) - current_index, 'bronze 1')
    
    return users
u = calculate_user_ranks(users)
for i in u:
    print('->', i)
