<%inherit file="/base.mako"/>

<%def name="content()">
	<form action="" method="post">
		<label for="last_to_nose_game_name">Last to Nose must...</label>
		<input class="long_text" type="text" name="last_to_nose_game_name" value="${name}"/>

		<h3>Participants</h3>
		<ul>
		% for seq, participant in enumerate(participants):
			<li>
				<input type="text" name="last_to_nose_participant_${seq}" value="${participant}"/>
			</li>
		% endfor
		</ul>

		<input type="submit"/>
	</form>
</%def>
