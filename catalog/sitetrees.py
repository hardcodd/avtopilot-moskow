from sitetree.utils import tree, item

sitetrees = (

    tree('breadcrumbs_catalog', 'Хлебные крошки для Каталога', items=[
        item('Главная', '/', url_as_pattern=False, children=[
            item('{{ instance.title }}', 'catalog_page instance.slug', url_as_pattern=True),
            item('{{ parent.title }}', 'catalog_page parent.slug', url_as_pattern=True, children=[
                item('{{ instance.title }}', 'products_category instance.slug', url_as_pattern=True)
            ]),
            item('Корзина', 'cart', url_as_pattern=True),
            item('Оформление заказа', 'order', url_as_pattern=True),
            item('{{ instance.back_title }}', 'catalog_page instance.back_link', url_as_pattern=True, children=[
                item('{{ instance.title }}', 'product_detail instance.slug', url_as_pattern=True)
            ]),
            item('Авточехлы', '/cases/', url_as_pattern=False, children=[
                item('{{ instance.title }}', 'make instance.slug', url_as_pattern=True),
                item('{{ instance.model.make.title }}', 'make instance.model.make.slug', url_as_pattern=True, children=[
                    item('{{ instance.title }}', 'case_detail instance.slug', url_as_pattern=True)
                ]),
            ]),
        ])
    ]),

)
