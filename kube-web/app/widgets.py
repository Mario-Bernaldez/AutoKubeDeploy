from django import forms
from django.utils.safestring import mark_safe


class HelpButtonTextInput(forms.TextInput):
    def __init__(self, *args, help_text=None, **kwargs):
        self.help_text = help_text
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        if self.help_text:
            help_id = f"{name}_help"
            button_id = f"{name}_toggle"

            help_button = f"""
                <button
                    type="button"
                    id="{button_id}"
                    aria-expanded="false"
                    aria-controls="{help_id}"
                    onclick="toggleHelp('{help_id}', '{button_id}')"
                    class="help-icon-button"
                >
                    ❔
                    <span class="visually-hidden">Mostrar ayuda para {name}</span>
                </button>
            """

            help_box = f"""
                <div id="{help_id}" role="tooltip" class="help-tooltip" style="display: none; margin: 0;">
                    {self.help_text}
                </div>
            """

            script = """
                <script>
                    function toggleHelp(helpId, buttonId) {
                        const help = document.getElementById(helpId);
                        const button = document.getElementById(buttonId);
                        const isVisible = help.style.display === 'inline-block';
                        help.style.display = isVisible ? 'none' : 'inline-block';
                        button.setAttribute('aria-expanded', !isVisible);
                    }
                </script>
            """

            return mark_safe(
                f"""
                <span class="help-wrapper" style="display: inline-flex; align-items: center; gap: 0.5rem;">
                    {input_html}
                    {help_button}
                    {help_box}
                </span>
                {script}
            """
            )
        return input_html


class HelpButtonCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, *args, help_text=None, **kwargs):
        self.help_text = help_text
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        checkboxes_html = super().render(name, value, attrs, renderer)
        if self.help_text:
            help_id = f"{name}_help"
            button_id = f"{name}_toggle"

            help_button = f"""
                <button
                    type="button"
                    id="{button_id}"
                    aria-expanded="false"
                    aria-controls="{help_id}"
                    onclick="toggleHelp('{help_id}', '{button_id}')"
                    class="help-icon-button"
                >
                    ❔
                    <span class="visually-hidden">Show help for {name}</span>
                </button>
            """

            help_box = f"""
                <div id="{help_id}" role="tooltip" class="help-tooltip" style="display: none; margin: 0;">
                    {self.help_text}
                </div>
            """

            script = """
                <script>
                    function toggleHelp(helpId, buttonId) {
                        const help = document.getElementById(helpId);
                        const button = document.getElementById(buttonId);
                        const isVisible = help.style.display === 'inline-block';
                        help.style.display = isVisible ? 'none' : 'inline-block';
                        button.setAttribute('aria-expanded', !isVisible);
                    }
                </script>
            """

            return mark_safe(
                f"""
                <div class="help-wrapper" style="display: inline-flex; align-items: flex-start; gap: 0.5rem;">
                    <div>{checkboxes_html}</div>
                    {help_button}
                    {help_box}
                </div>
                {script}
            """
            )
        return checkboxes_html


class HelpButtonSelect(forms.Select):
    def __init__(self, *args, help_text=None, **kwargs):
        self.help_text = help_text
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        select_html = super().render(name, value, attrs, renderer)
        if self.help_text:
            help_id = f"{name}_help"
            button_id = f"{name}_toggle"

            help_button = f"""
                <button
                    type="button"
                    id="{button_id}"
                    aria-expanded="false"
                    aria-controls="{help_id}"
                    onclick="toggleHelp('{help_id}', '{button_id}')"
                    class="help-icon-button"
                    style="margin-left: 0.5rem;"
                >
                    ❔
                    <span class="visually-hidden">Show help for {name}</span>
                </button>
            """

            help_box = f"""
                <div id="{help_id}" role="tooltip" class="help-tooltip"
                     style="display: none; margin-left: 0.5rem;">
                    {self.help_text}
                </div>
            """

            script = """
                <script>
                    function toggleHelp(helpId, buttonId) {
                        const help = document.getElementById(helpId);
                        const button = document.getElementById(buttonId);
                        const isVisible = help.style.display === 'inline-block';
                        help.style.display = isVisible ? 'none' : 'inline-block';
                        button.setAttribute('aria-expanded', !isVisible);
                    }
                </script>
            """

            return mark_safe(
                f"""
                <span class="help-wrapper" style="display: inline-flex; align-items: center;">
                    {select_html}
                    {help_button}
                    {help_box}
                </span>
                {script}
            """
            )
        return select_html


class HelpButtonCheckboxInput(forms.CheckboxInput):
    def __init__(self, *args, help_text=None, **kwargs):
        self.help_text = help_text
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        checkbox_html = super().render(name, value, attrs, renderer)
        if self.help_text:
            help_id = f"{name}_help"
            button_id = f"{name}_toggle"

            help_button = f"""
                <button
                    type="button"
                    id="{button_id}"
                    aria-expanded="false"
                    aria-controls="{help_id}"
                    onclick="toggleHelp('{help_id}', '{button_id}')"
                    class="help-icon-button"
                    style="margin-left: 0.5rem;"
                >
                    ❔
                    <span class="visually-hidden">Show help for {name}</span>
                </button>
            """

            help_box = f"""
                <div id="{help_id}" role="tooltip" class="help-tooltip"
                     style="display: none; margin-left: 0.5rem;">
                    {self.help_text}
                </div>
            """

            script = """
                <script>
                    function toggleHelp(helpId, buttonId) {
                        const help = document.getElementById(helpId);
                        const button = document.getElementById(buttonId);
                        const isVisible = help.style.display === 'inline-block';
                        help.style.display = isVisible ? 'none' : 'inline-block';
                        button.setAttribute('aria-expanded', !isVisible);
                    }
                </script>
            """

            return mark_safe(
                f"""
                <span class="help-wrapper" style="display: inline-flex; align-items: center;">
                    {checkbox_html}
                    {help_button}
                    {help_box}
                </span>
                {script}
            """
            )
        return checkbox_html


class HelpButtonTextarea(forms.Textarea):
    def __init__(self, *args, help_text=None, **kwargs):
        self.help_text = help_text
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        textarea_html = super().render(name, value, attrs, renderer)
        if self.help_text:
            help_id = f"{name}_help"
            button_id = f"{name}_toggle"

            help_button = f"""
                <button
                    type="button"
                    id="{button_id}"
                    aria-expanded="false"
                    aria-controls="{help_id}"
                    onclick="toggleHelp('{help_id}', '{button_id}')"
                    class="help-icon-button"
                    style="margin-left: 0.5rem;"
                >
                    ❔
                    <span class="visually-hidden">Show help for {name}</span>
                </button>
            """

            help_box = f"""
                <div id="{help_id}" role="tooltip" class="help-tooltip"
                     style="display: none; margin-left: 0.5rem;">
                    {self.help_text}
                </div>
            """

            script = """
                <script>
                    function toggleHelp(helpId, buttonId) {
                        const help = document.getElementById(helpId);
                        const button = document.getElementById(buttonId);
                        const isVisible = help.style.display === 'inline-block';
                        help.style.display = isVisible ? 'none' : 'inline-block';
                        button.setAttribute('aria-expanded', !isVisible);
                    }
                </script>
            """

            return mark_safe(
                f"""
                <span class="help-wrapper" style="display: inline-flex; align-items: flex-start;">
                    {textarea_html}
                    {help_button}
                    {help_box}
                </span>
                {script}
            """
            )
        return textarea_html


class HelpButtonNumberInput(forms.NumberInput):
    def __init__(self, *args, help_text=None, **kwargs):
        self.help_text = help_text
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        if self.help_text:
            help_id = f"{name}_help"
            button_id = f"{name}_toggle"

            help_button = f"""
                <button
                    type="button"
                    id="{button_id}"
                    aria-expanded="false"
                    aria-controls="{help_id}"
                    onclick="toggleHelp('{help_id}', '{button_id}')"
                    class="help-icon-button"
                    style="margin-left: 0.5rem;"
                >
                    ❔
                    <span class="visually-hidden">Show help for {name}</span>
                </button>
            """

            help_box = f"""
                <div id="{help_id}" role="tooltip" class="help-tooltip"
                     style="display: none; margin-left: 0.5rem;">
                    {self.help_text}
                </div>
            """

            script = """
                <script>
                    function toggleHelp(helpId, buttonId) {
                        const help = document.getElementById(helpId);
                        const button = document.getElementById(buttonId);
                        const isVisible = help.style.display === 'inline-block';
                        help.style.display = isVisible ? 'none' : 'inline-block';
                        button.setAttribute('aria-expanded', !isVisible);
                    }
                </script>
            """

            return mark_safe(
                f"""
                <span class="help-wrapper" style="display: inline-flex; align-items: center;">
                    {input_html}
                    {help_button}
                    {help_box}
                </span>
                {script}
            """
            )
        return input_html
