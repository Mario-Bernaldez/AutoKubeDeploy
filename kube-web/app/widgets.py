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

            return mark_safe(f"""
                <span class="help-wrapper" style="display: inline-flex; align-items: center; gap: 0.5rem;">
                    {input_html}
                    {help_button}
                    {help_box}
                </span>
                {script}
            """)
        return input_html
