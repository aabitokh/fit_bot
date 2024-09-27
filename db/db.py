exersices: dict[str, str] = {
                            'Грудь 🏋🏻':'chest_training', 
                            'Плечи 🎾': 'shoulders_trainig', 
                            'Ноги 🚵🏻‍♂️' : 'legs_training', 
                            'Спина 🏊🏻‍♂️' : 'back_training',
                            'Руки 🦾' : 'arms'
                        }

exersices_for_muscle_group: dict[str, dict[str, str]] = {
                                                        'chest_training': {
                                                                            'Жим лежа': 'bench_press', 
                                                                            'Жим лежа под углом': 'bench_press_up', 
                                                                            'Разводка на грудь': 'breast_dilution', 
                                                                            'Брусья': 'bars'
                                                                            }, 

                                                        'shoulders_trainig': {
                                                                            'Жим сидя в тренажере' : 'shoulders_press', 
                                                                            'Махи гантелями' : 'swing_dumbbells', 
                                                                            'Отведение на заднюю дельту' : 'posterior_delta'
                                                                            }, 
                                                        'legs' : {
                                                            'Присед' : 'squat',
                                                            'Румныская тяга' : 'dead_lift', 
                                                            'Разгибание ног' : 'leg_extension'
                                                        }, 
                                                        'back': {
                                                            'Подтягивания': 'pull_ups', 
                                                            'Тяга вертикального блока в рычагах': 'vertical_block_lift',
                                                            'Тяга горизонтального блока': 'horisontal_block_lift',
                                                        },
                                                        'arms': {
                                                            'ПШНБ': 'pshnb', 
                                                            'Разгибания на блоке на трицепс': 'extensions_on_the_triceps_block',
                                                            'Молотки': 'dumbbells',
                                                            'Разгибания с гантелями на трицепс': 'dumbbells_triceps'
                                                        }
                                                                    
                                                    }

exc_list = []

for key_exc in exersices_for_muscle_group.keys():
    for key in exersices_for_muscle_group[key_exc]:
        exc_list.extend(list(exersices_for_muscle_group[key_exc].values()))