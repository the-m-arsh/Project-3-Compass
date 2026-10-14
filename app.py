"""Gradio app for Compass. Run with: uv run app.py"""

import html

import gradio as gr

import styles
from compass import Compass

LAUNCH_STYLE = {"theme": styles.THEME, "css": styles.CSS, "head": styles.JS}

HEADER = """
<div id="header">
    <h1>Compass</h1>
    <div class="brand-bar"></div>
</div>
"""


def render_todos(todos):
    if not todos:
        items = '<div class="placeholder">Compass will write its plan here as it works</div>'
    else:
        items = "<ul>" + "".join(
            f'<li class="{todo["status"]}"><span class="mark"></span>{html.escape(todo["content"])}</li>'
            for todo in todos
        ) + "</ul>"
    return f"<h3>Plan</h3>{items}"


async def setup():
    compass = Compass()
    await compass.setup()
    return compass, gr.update(interactive=True)


async def process_message(compass, message, history):
    if compass is None:  # the user clicked before setup finished bringing up the MCP servers
        return history, gr.update(visible=False), compass, gr.update(), gr.update(), gr.update()
    results = await compass.run_turn(message, history)
    # This was the first message of the conversation. From here on, the reply box takes over:
    # disable the message box and the Go button, and reveal the reply box in their place.
    return (
        results,
        gr.update(visible=compass.paused),
        compass,
        gr.update(interactive=False),
        gr.update(visible=True, interactive=True),
        gr.update(interactive=False),
    )


async def process_reply(compass, reply_text, history):
    if compass is None:
        return history, gr.update(visible=False), compass
    results = await compass.reply(reply_text, history)
    return results, gr.update(visible=compass.paused), compass


async def approve(compass, history):
    results = await compass.resume(history)
    return results, gr.update(visible=compass.paused), compass


def watch_todos(compass):
    """Called by the timer. The timer is the plan panel's only writer: if a long-running
    event owned the panel as an output, Gradio would lock it as pending and live updates
    would not render while Compass works."""
    return render_todos(compass.todos) if compass else render_todos([])


async def reset(compass):
    if compass:
        compass.cleanup()
    new_compass = Compass()
    await new_compass.setup()
    # Put the message box back in charge and hide the reply box, exactly like a fresh page load.
    return (
        gr.update(value="", interactive=True),
        gr.update(value="", visible=False, interactive=False),
        None,
        gr.update(visible=False),
        new_compass,
        gr.update(interactive=True),
    )


def free_resources(compass):
    if compass:
        compass.cleanup()


with gr.Blocks(title="Compass") as ui:
    gr.HTML(HEADER)
    compass = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Compass", height=320, scale=3, elem_id="chat")
        with gr.Column(scale=1):
            todos_panel = gr.HTML(render_todos([]), elem_id="plan-panel")
    with gr.Group(elem_id="ask-panel"):
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to Compass")
        with gr.Row():
            reply_box = gr.Textbox(
                show_label=False, placeholder="Reply to Compass", visible=False, interactive=False
            )
    with gr.Row():
        reset_button = gr.Button("Reset", elem_id="reset-button")
        approve_button = gr.Button("Approve and continue", visible=False, elem_id="approve-button")
        go_button = gr.Button("Go!", elem_id="go-button", interactive=False)

    timer = gr.Timer(1)

    ui.load(setup, [], [compass, go_button])
    timer.tick(watch_todos, [compass], [todos_panel], show_progress="hidden")
    message.submit(process_message, [compass, message, chatbot],
                   [chatbot, approve_button, compass, message, reply_box, go_button])
    go_button.click(process_message, [compass, message, chatbot],
                    [chatbot, approve_button, compass, message, reply_box, go_button])
    reply_box.submit(process_reply, [compass, reply_box, chatbot],
                     [chatbot, approve_button, compass])
    approve_button.click(approve, [compass, chatbot], [chatbot, approve_button, compass])
    reset_button.click(reset, [compass],
                       [message, reply_box, chatbot, approve_button, compass, go_button])


if __name__ == "__main__":
    ui.launch(inbrowser=True, **LAUNCH_STYLE)