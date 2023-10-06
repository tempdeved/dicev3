import dash_bootstrap_components as dbc

from elements.element import Component

class Accordion(object):

    def __init__(self):
        ...

    def load(self, id, accordion_title, elements: list = []):

        layout = dbc.Accordion(
            id=f'{id}-accordion',
            start_collapsed=False,
            class_name='mx-0 px-0 my-0 py-0 accordion-button-bg-secondary shadow-lg',
            flush=True,
            children=dbc.AccordionItem(
                class_name='mx-0 px-0 py-0 my-0',
                title=accordion_title,
                children=elements
            ),
        )

        return layout