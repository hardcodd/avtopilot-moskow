from sitetree.utils import tree, item

sitetrees = (

    tree('breadcrumbs_pages', 'Хлебные крошки для Страниц', items=[
        item('Главная', '/', url_as_pattern=False, children=[
            item('{{ instance.title }}', 'contacts', url_as_pattern=True),
            item('{{ instance.title }}', 'team', url_as_pattern=True),
            item('{{ instance.title }}', 'help instance.slug', url_as_pattern=True),
            item('{{ instance.title }}', 'info instance.slug', url_as_pattern=True),
            item('{{ instance.title }}', 'staff instance.slug', url_as_pattern=True),
            item('{{ instance.title }}', 'portfolio instance.slug', url_as_pattern=True),
            item('{{ instance.title }}', 'about instance.slug', url_as_pattern=True),
        ])
    ]),

)
