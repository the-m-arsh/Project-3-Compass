"""Look and feel for the Compass app: white text on dark gray, with orange as the single
accent color throughout.
In Gradio 6, theme, css and js are passed to launch() rather than to gr.Blocks()."""

import gradio as gr

TEXT = "#F2F2F2"
ORANGE = "#FF9800"
ORANGE_DARK = "#F57C00"
GRAY = "#AAAAAA"
BACKGROUND = "#1C1C1C"
PANEL = "#2A2A2A"
BORDER = "#3A3A3A"
RED = "#FF5252"
RED_DARK = "#BC101F"

THEME = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#FFF3E0", c100="#FFE0B2", c200="#FFCC80", c300="#FFB74D", c400="#FFA726",
        c500="#FF9800", c600="#FB8C00", c700="#F57C00", c800="#EF6C00", c900="#E65100",
        c950="#BF360C",
    ),
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Montserrat"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=["Courier New", "ui-monospace", "monospace"],
)

CSS = """
.gradio-container { background: #1C1C1C !important; }

#header { padding: 4px 2px 2px; }
#header h1 { color: #F2F2F2; font-weight: 700; font-size: 30px; margin: 2px 0 8px; }
#header .brand-bar {
    height: 4px; width: 132px; border-radius: 2px;
    background: #FF9800;
}

#chat, #plan-panel, #ask-panel {
    background: #2A2A2A; border: 1px solid #3A3A3A; border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
}

#chat .message { font-size: 14px; color: #F2F2F2; }

#plan-panel { padding: 16px 18px; }
#plan-panel h3 {
    color: #FF9800; font-size: 12px; font-weight: 700;
    letter-spacing: 0.18em; text-transform: uppercase; margin: 0 0 10px;
}
#plan-panel .placeholder { color: #AAAAAA; font-size: 13px; font-style: italic; }
#plan-panel ul { list-style: none; padding: 0; margin: 0; }
#plan-panel li {
    color: #F2F2F2; font-size: 13px; line-height: 1.45;
    margin: 8px 0; display: flex; align-items: baseline; gap: 8px;
}
#plan-panel .mark {
    flex: none; width: 12px; height: 12px; border-radius: 50%;
    position: relative; top: 1px;
}
#plan-panel li.pending .mark { border: 2px solid #FFB74D; background: #2A2A2A; }
#plan-panel li.in_progress .mark { border: 2px solid #FF9800; background: #FFCC80; }
#plan-panel li.completed .mark { border: 2px solid #AAAAAA; background: #F2F2F2; }
#plan-panel li.completed { color: #AAAAAA; }

#ask-panel { padding: 6px; }
#ask-panel textarea { color: #F2F2F2; font-size: 14px; }
#ask-panel textarea::placeholder { color: #AAAAAA; }

#go-button {
    background: #FF9800 !important; color: #FFFFFF !important; border: none !important;
    font-weight: 600; box-shadow: 0 2px 8px rgba(255, 152, 0, 0.35);
}
#go-button:hover { background: #F57C00 !important; }
#approve-button {
    background: transparent !important; color: #FF9800 !important; border: 2px solid #FF9800 !important;
    font-weight: 700; box-shadow: none;
}
#approve-button:hover { background: rgba(255, 152, 0, 0.1) !important; }
#reset-button {
    background: #2A2A2A !important; color: #FF5252 !important;
    border: 1px solid #FF5252 !important; font-weight: 600;
}
#reset-button:hover { background: #BC101F !important; color: #FFFFFF !important; }
"""

# The brand is dark mode, so steer Gradio away from the system light preference.
# Served via launch(head=JS), so it runs before the app mounts and there is no light flash.
JS = """
<script>
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.replace(url.href);
    }
</script>
"""