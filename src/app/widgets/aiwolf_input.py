from textual.widgets import Input, LoadingIndicator


class AIWolfNLPInput(Input):
    def __init__(
        self,
        value=None,
        placeholder="",
        highlighter=None,
        password=False,
        *,
        restrict=None,
        type="text",
        max_length=0,
        suggester=None,
        validators=None,
        validate_on=None,
        valid_empty=False,
        select_on_focus=True,
        name=None,
        id=None,
        classes=None,
        disabled=False,
        tooltip=None,
    ):
        super().__init__(
            value,
            placeholder,
            highlighter,
            password,
            restrict=restrict,
            type=type,
            max_length=max_length,
            suggester=suggester,
            validators=validators,
            validate_on=validate_on,
            valid_empty=valid_empty,
            select_on_focus=select_on_focus,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            tooltip=tooltip,
        )

    def enable(self) -> None:
        self.disabled = False

        if self.children:
            self.remove_children()

    def disable(self) -> None:
        self.disabled = True
        self.mount(LoadingIndicator(id="loading"))

    def toggle_availability(self) -> None:
        if self.disabled:
            self.enable()
        else:
            self.disable()
