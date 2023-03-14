"""Browse images from online repositories and load their latent AI creation data."""

import os
import json
import requests
import gradio as gr

from modules import script_callbacks
from modules.generation_parameters_copypaste import create_buttons, ParamBinding, register_paste_params_button

_root = os.path.dirname(os.path.abspath(__file__))
try:
    with open(f"{_root}/service.json", 'r', encoding='utf-8') as data:
         _SERVICE = json.load(data)
except Exception as e:
    print(e)
    exit(-1)

def api_search_service(text, service):
    session = requests.Session()
    session.headers.update({'User-Agent': 'ai-looking-for-friends'})
    key_out = service['key_out']
    url = f"{service['url_find']}{text}"
    blob = session.get(url, timeout=4)
    blob = blob.json()

    if (newdata := blob.get(key_out, None)) is None:
        return [], []

    # skipping entries that are stored in rails storage not at CDN
    # keeping only 10 results from all services...
    key_img = service['key_img']
    newdata = [d for d in newdata if (check := d.get(key_img, None)) and check[0] != '/'][:10]

    out_data = []
    out_img = []
    mapper = service.get("map", {})
    for entry in newdata:
        if (nimg := entry.pop(key_img)) is None:
            continue

        out_img.append(nimg)
        if (meta := entry.get('metadata', None)):
            entry.update(meta)
            entry.pop('metadata')

        data = {}
        for field, value in entry.items():
            if (v := mapper.get(field, None)):
                data[v] = value
        out_data.append(data)

    return out_img, out_data

def api_search(text, state_check):
    out_msg = ''
    out_data = []
    out_gallery = []

    for who, service in _SERVICE.items():
        if who != 'prompthero' and who not in state_check:
            out_gallery.append([])
            continue

        print(f'{who} [query] => {text}')
        try:
            img, prompt = api_search_service(text, service)
        except Exception as e:
            print(e)
        else:
            out_gallery.append(img)
            if (mapper := service.get("map", None)) is None:
                continue

            for e in prompt:
                data = {}
                for k, t in mapper.items():
                    if (v := e.get(k, None)) is None:
                        continue
                    data[t] = v
                out_data.append(data)

            out_msg = f'==> {who} - {len(img)}\n{out_msg}'

    if (size := len(out_data)) < 1:
        out_msg = f'no matches\n{out_msg}'
    else:
        out_msg = f'{size} matches found\n{out_msg}'
    return out_msg, out_data, *out_gallery

def ui():
    with gr.Blocks() as browser:
        with gr.Row(visible=False):
            gr.Textbox(value=-2, elem_id="ph_field_index")
            but_refresh = gr.Button('', elem_id="ph_but_refresh")
            field_metadata = gr.JSON(elem_id="ph_metadata")
            field_image = gr.Image(None, type='pil', elem_id="ph_image")

        with gr.Row(variant="panel"):
            with gr.Column(variant="compact", scale=6):
                with gr.Row():
                    with gr.Column(variant="compact", scale=4):
                        field_search = gr.Textbox(
                            label="search",
                            show_label=False,
                            lines=1,
                            max_lines=1,
                            placeholder="search artwork on PromptHero.com...",
                        ).style(container=False)

                    with gr.Column(variant="compact"):
                        name = list(_SERVICE)
                        name.pop(0)
                        check_service = gr.CheckboxGroup(name, show_label=False, interactive=True)

                with gr.Row():
                    with gr.Column():
                        services = {}
                        for k in _SERVICE:
                            grid = 6
                            accord = None
                            if k == 'prompthero':
                                accord = gr.Accordion(_SERVICE[k]['name'], visible=False)
                                gallery = gr.Gallery(elem_id=f"field_gallery_{k}")
                            else:
                                grid = 12
                                with gr.Accordion(_SERVICE[k]['name'], open=False) as accord:
                                    gallery = gr.Gallery(elem_id=f"field_gallery_{k}")

                            gallery.update(show_label=False)
                            gallery.style(grid=grid, preview=True)

                            services[k] = {
                                'gallery': gallery,
                                'accord': accord
                            }

            with gr.Column(variant="compact", scale=4):
                field_message = gr.Textbox(
                    label="message",
                    show_label=False,
                    lines=3,
                    max_lines=3,
                    interactive=False,
                    visible=False
                ).style(container=False)

                with gr.Row(variant="compact"):
                    send_to_buttons = create_buttons(["txt2img", "img2img"])

                with gr.Row(variant="compact"):
                    send_to_buttons.update(create_buttons(["inpaint", "extras"]))

                field_selection = gr.Textbox(
                    show_label=False,
                    elem_id="ph_selection"
                )

                for tabname, button in send_to_buttons.items():
                    register_paste_params_button(ParamBinding(
                        tabname=tabname,
                        paste_button=button,
                        source_text_component=field_selection,
                        source_image_component=field_image
                    ))

            gallery = [services[d]['gallery'] for d in _SERVICE.keys()]
            # accord = [services[d]['accord'] for d in _SERVICE.keys()]
            # cant get the accordians to hide...
            # check_service.change(lambda a: [gr.update(visible=v in a) for v in check_service.value], check_service, *accord)
            field_search.submit(api_search, [field_search, check_service], [field_message, field_metadata, *gallery])
            but_refresh.click(None, _js="ph_current_index", inputs=[field_metadata], outputs=[field_selection])

    browser.queue()
    return (browser, 'PromptHero', 'tab_prompthero'),

script_callbacks.on_ui_tabs(ui)
