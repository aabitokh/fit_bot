from dataclasses import dataclass, field
from typing import Optional, Dict, List



class Training: 

    def __init__(self, data) -> None:
        self.data = data
        self.start_training = self.data['start_training']
        
        # Инициализируем список мышечных групп
        self.muscle_groups = list(self.data['muscle_group'].keys())  # Используем ключи для обозначения мышечных групп
        
        # Инициализируем список названий выполненных упражнений
        self.done_exercises = [exercise for mg in self.muscle_groups for exercise in self.data['muscle_group'][mg].keys()]

        self.tonnage = {}
        
        # Вычисляем тоннаж для каждого упражнения
        for mg in self.muscle_groups:
            for exercise, sets in self.data['muscle_group'][mg].items():
                total_weight = 0
                for set_str in sets:
                    # Обработка строки с весами и повторениями
                    set_data = set_str.split(', ')
                    for weight_rep in set_data:
                        weight, reps = map(int, weight_rep.split(' '))
                        total_weight += weight * reps
                self.tonnage[exercise] = total_weight

