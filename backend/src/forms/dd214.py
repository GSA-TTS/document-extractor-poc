from src.forms.form import Form


class DDTwoOneFour(Form):
    def identifier(self) -> str:
        return "DD214"

    def form_matches(self) -> str:
        return "DD FORM 214"

    def queries(self) -> list[str]:
        return []
