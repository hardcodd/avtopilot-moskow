from sitetree.utils import tree, item

sitetrees = (

    tree('breadcrumbs_vacations', 'Хлебные крошки для Вакансий', items=[
        item('Главная', '/', url_as_pattern=False, children=[
            item('{{ instance.title }}', 'vacations', url_as_pattern=True),
        ])
    ]),

)
