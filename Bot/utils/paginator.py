from interactions.ext.paginators import Page, Paginator

class CustomPaginator(Paginator):
    def __init__(self, *args, custom_buttons=None, start_page=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_buttons = custom_buttons or []
        self.page_index = start_page

    @classmethod
    def create_from_embeds(cls, client, *embeds, **kwargs):
        """Pass embeds directly to the paginator instead of creating Pages"""
        start_page = kwargs.pop('start_page', 0)
        return cls(client, pages=list(embeds), start_page=start_page, **kwargs)

    def to_dict(self):
        """Convert paginator to dict with custom buttons"""
        paginator_dict = super().to_dict()
        
        if self.custom_buttons and paginator_dict["components"]:
            if len(self.custom_buttons) > self.page_index + 1:
                custom_row = self.custom_buttons[self.page_index + 1]
                paginator_dict["components"].append(custom_row.to_dict())

            if self.custom_buttons:  # Add common buttons
                custom_row = self.custom_buttons[0]
                paginator_dict["components"].append(custom_row.to_dict())
        
        return paginator_dict