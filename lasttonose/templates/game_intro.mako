<%inherit file="/base.mako"/>

<%def name="content()">
	<h3>Last to Nose must...<span class="game_name">${game['name']}</span></h3>
	
	<div class="nose-touch-status">
		% for participant in game['participants']:
		<div class="participant">
				<form action="/touch_nose" method="post" class="nose-touch">
					<input type="hidden" name="game" value="${game['_id']}"/>
					<input type="hidden" name="participant" value="${participant['name']}"/>
					<input type="image" src="/static/images/nose.jpg"; value="Touch your nose!"/>
				</form>
				<p class="name">${participant['name']}</p>
		</div>
		% endfor
	</div>
</%def>
