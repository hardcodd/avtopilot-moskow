from sitetree.utils import tree, item

sitetrees = (

    tree('breadcrumbs_account', 'Хлебные крошки для Аккаунтов', items=[
        item('Главная', '/', url_as_pattern=False, children=[
            item('Профиль', '/account/', url_as_pattern=True),
            item('Логин', '/login/', url_as_pattern=True),
            item('Регистрация', '/registration/', url_as_pattern=True),
        ])
    ]),

)
