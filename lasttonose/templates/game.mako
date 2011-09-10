<h2>Last To Nose must <span class="game_name">${game['name']}</span></h2>
    % if game_state.game_over:
    <h3>Game Over! ${game_state.loser} must ${game['name']}!</h3>
    % endif

    % for participant in game['participants']:
    <div class="participant">
        % if participant['touched_nose']:
            <p class="touched_nose">${participant['name']} Has Touched Nose!</p>
        % else:
            <p class="not_touched_nose">${participant['name']} has not Touched Nose!</p>
        % endif
     </div>
% endfor
