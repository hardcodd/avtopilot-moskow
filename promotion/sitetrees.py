from sitetree.utils import tree, item

sitetrees = (

    tree('breadcrumbs_promotion', 'Хлебные крошки для Акций', items=[
        item('Главная', '/', url_as_pattern=False, children=[
            item('{{ instance.title }}', 'promotion instance.slug', url_as_pattern=True),
            item('Акции', '/promotion/', url_as_pattern=False, children=[
                item('{{ instance.title }}', 'promotion_category instance.slug', url_as_pattern=True)
            ]),
            item('Акции', '/promotion/', url_as_pattern=False, children=[
                item('{{ instance.category.title }}', 'promotion_category instance.category.slug', url_as_pattern=True,
                     children=[
                         item('{{ instance.title }}', 'promotion_detail instance.slug', url_as_pattern=True)
                     ])
            ]),
        ])
    ]),

)
