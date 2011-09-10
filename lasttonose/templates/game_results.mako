<%inherit file="/base.mako"/>

<%def name="content()">
    <h3>Last To Nose must... <span class="game_name">${game_name}</span></h3>
    %if game_state.game_over:
        <h3>Game Over! ${game_state.loser} must ${game_name}!</h3>
    % endif

	<div class="nose-touch-status">
		% for (name, participant), image_number in zip(participants, participant_image_numbers):
		<div class="participant ${'touched_nose' if participant['touched_nose'] else 'not_touched_nose'}">
			%if participant['touched_nose']:
				<img class="status" src="/static/images/touched_nose_${image_number}.jpg" alt="${name} touched their nose"/>
			%else:
				<img class="status" src="/static/images/not_touched_nose_${image_number}.jpg" alt="${name} hasn't touched their nose"/>
			%endif
			<p class="name">${name}</p>
		</div>
		% endfor
	</div>
</%def>
