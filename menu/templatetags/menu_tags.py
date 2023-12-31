from django import template

from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/items.html')
def get_submenu(menu_name, item_name):
    """Template tag, который возвращает нарисованное меню с учётом выбранных пунктов и подпунктов в интерфейсе."""
    items = MenuItem.objects.filter(menu__name=menu_name)

    def get_menu(first_menu: str = None, second_menu: list = None):
        """Функция рекурсивно конструирует и возвращает, после конструирования,
        меню с учётом его пунктов и подпунктов у пунктов."""
        if first_menu is None:
            menu = list(items.filter(parent__name=None))
            if second_menu is None:
                return menu
            try:
                menu.insert(menu.index(second_menu[0].parent) + 1, second_menu)
            except ValueError:
                submenu = get_menu(first_menu=second_menu[0].parent, second_menu=second_menu)
                menu = get_menu(second_menu=submenu)
            return menu

        elif first_menu and second_menu:
            first_menu = list(items.filter(name=first_menu))[0]
            menu = list(items.filter(parent__name=first_menu.parent))
            menu.insert(menu.index(second_menu[0].parent) + 1, second_menu)
            return menu

        else:
            menu = list(items.filter(parent__name=first_menu))
            if not menu:
                child = list(items.filter(name=first_menu))
                return get_menu(first_menu=child[0].parent)
            menu = get_menu(second_menu=menu)
            return menu

    if menu_name == item_name:
        return {'items': get_menu()}
    else:
        return {'items': get_menu(item_name)}
