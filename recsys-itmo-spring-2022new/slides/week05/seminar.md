# Семинар 5. Разнообразие рекомендаций

На этом семинаре посмотрим, как влияет разнообразие выдачи на удовлетворение пользователя.
Сравним два item-to-item рекомендера:
- рекомендующий любой трек, похожий на предыдущий (_жадный_)
- рекомендующий трек, похожий на предыдущий но другого исполнителя (_разнообразный_)

### План действий

1.  Используем ноутбук `Week5SeminarModel.ipynb`, обучить lightfm и подготовить рекомендации
    1. Собираем данные и обучаем lightfm аналогично 3 семинару
    2. Пишем функцию, которая готовит рекомендации:
        1. К каждому треку составляем список рекомендованных как в 4 семинаре
        2. Параметр `max_tracks_from_same_artist` регулирует, сколько треков может повторяться от одного исполнителя
        3. Данные пишем в том же формате как и в 4 семинаре
    
2. Запускаем два A/B эксперимента.
    1. Один для _жадного_ рекомендера
    2. Один для _разнообразного_
   
3. Используем ноутбук `Week1Seminar.ipynb` для анализа.
    1. Сравниваем результаты.
    
Вопросы
    1. Как более честно сравнить рекомендеры?
    2. Как подобрать ниалучший `max_tracks_from_same_artist`?
