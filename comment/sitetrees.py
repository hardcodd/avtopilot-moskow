from sitetree.utils import tree, item

sitetrees = (

    tree('breadcrumbs_comment', 'Хлебные крошки для Комментариев', items=[
        item('Главная', '/', url_as_pattern=False, children=[
            item('{{ instance.title }}', 'add_review_action', url_as_pattern=True),
        ])
    ]),

)
