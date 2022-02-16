import json

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    with open('entities.json', encoding='utf-8') as f:
        entities = json.load(f)
        return render_template("main-all-items.html", entities=entities)


@app.route('/paging')
def paging():
    count_item = 3
    with open('entities.json', encoding='utf-8') as f:
        entities = json.load(f)
    all_items = len(entities)
    current_page = int(request.args.get('p', 1))
    l_page = all_items // count_item
    items_show = entities[(current_page - 1) * count_item:current_page * count_item]
    return render_template("main.html", entities=items_show, all_items=all_items, l_page=l_page,
                           current_page=current_page)


@app.route('/search')
def search():
    model = request.args.get('model')
    with open('entities.json', encoding='utf-8') as f:
        entities = json.load(f)
        response = []
        if not model:
            response = entities
        else:
            for e in entities:
                if e["model"] == model:
                    response.append(e)
            if len(response) == 0:
                model_split = model.split(" ")
                for e in entities:
                    source_find = e["model"]
                    if source_find.split(" ")[0] == model_split[0]:
                        response.append(e)
                if len(response) == 0 and " " in model:
                    for e in entities:
                        source_find = e["model"]
                        if " " in source_find:
                            if source_find.split(" ")[1] == model_split[1]:
                                response.append(e)
                else:
                    for e in entities:
                        source_find = e["model"]
                        if " " in source_find:
                            if source_find.split(" ")[1] == model:
                                response.append(e)

        return render_template("search_ause.html", entities=response)


@app.route('/card/<int:eid>')
def card(eid: int):
    with open('entities.json', encoding='utf-8') as f:
        entities = json.load(f)
        for ent in entities:
            if ent["id"] == eid:
                return render_template("card_full.html", entity=ent)


@app.route('/card/<int:eid>/short')
def card_short(eid: int):
    with open('entities.json', encoding="utf-8") as f:
        entities = json.load(f)
        for ent in entities:
            if ent["id"] == eid:
                return render_template("short_card.html", entity=ent)


if __name__ == '__main__':
    app.run(debug=True)
