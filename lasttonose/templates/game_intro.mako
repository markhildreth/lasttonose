<h2>Last to Nose must <span class="game_name">${game['name']}</span></h2>
% for participant in game['participants']:
    <div>
        <h2>${participant['name']}</h2>
        <form action="/touch_nose" method="post">
            <input type="hidden" name="game" value="${game['_id']}"/>
            <input type="hidden" name="participant" value="${participant['name']}"/>
            <input type="submit" value="${participant['name']}, touch your nose!"/>
        </form>
% endfor
